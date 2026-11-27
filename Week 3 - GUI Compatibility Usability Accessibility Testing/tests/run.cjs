const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const { spawn } = require('node:child_process');
const { chromium, firefox, webkit, devices } = require('playwright');
const axe = require('axe-core');

const root = path.resolve(__dirname, '..');
const deviceMode = process.argv.includes('--devices');
const logName = name => path.join(root, 'logs', deviceMode ? 'devices-' + name : name);
const deviceProfiles = [
  { engine: 'webkit', descriptor: 'iPhone 15' },
  { engine: 'chromium', descriptor: 'Pixel 7' },
  { engine: 'chromium', descriptor: 'Galaxy S24' },
  { engine: 'webkit', descriptor: 'iPad Pro 11' },
];
const baseURL = 'http://127.0.0.1:51793';
const run = { started: new Date().toISOString(), os: os.release(), node: process.version,
  playwright: require('playwright/package.json').version, axe: axe.version, configurations: [], cases: [] };
const serverLog = fs.openSync(logName('flask.log'), 'w');
const server = spawn(process.env.QA_PYTHON || 'python', ['-B', path.join(__dirname, 'server.py'), '51793'],
  { stdio: ['ignore', serverLog, serverLog] });
fs.closeSync(serverLog);
let startupError;
server.on('error', error => { startupError = error; });
const password = 'Week3_valid!';
const viewports = [
  { name: 'desktop', width: 1440, height: 900, mobile: false },
  { name: 'tablet', width: 768, height: 1024, mobile: true },
  { name: 'mobile', width: 390, height: 844, mobile: true },
];

const link = (p, name) => p.getByRole('link', { name, exact: true });
const button = (p, name) => p.getByRole('button', { name, exact: true });
const field = (p, name) => p.locator(`[name="${name}"]`);
const row = (p, title) => p.locator('tbody tr').filter({ hasText: title });
const text = async (locator) => (await locator.innerText()).trim();
async function submit(p, locator, pathname) {
  await Promise.all([p.waitForURL(url => url.pathname === pathname, { waitUntil: 'load' }), locator.click()]);
}
async function credentials(p, user, secret = password) {
  await field(p, 'username').fill(user);
  await field(p, 'password').fill(secret);
}
async function register(p, user) {
  await p.goto('/register');
  await credentials(p, user);
  await submit(p, button(p, 'Register'), '/');
}
async function taskForm(p, title, category = 'Work', due = '2099-04-10') {
  await field(p, 'title').fill(title);
  await field(p, 'description').fill('Week 3 fixture description');
  await field(p, 'category_id').selectOption({ label: category });
  await field(p, 'due_date').fill(due);
}
async function create(p, title, category, due) {
  await p.goto('/tasks/new');
  await taskForm(p, title, category, due);
  await submit(p, button(p, 'Create Task'), '/');
}
async function filter(p, name, value) {
  await Promise.all([p.waitForNavigation(), field(p, name).selectOption(value)]);
}
async function screenshot(p, category, name, viewportOnly = false) {
  const evidence = `screenshots/${category}${deviceMode ? "/devices" : ""}/${name}.png`;
  fs.mkdirSync(path.dirname(path.join(root, evidence)), { recursive: true });
  await p.screenshot({ path: path.join(root, evidence), fullPage: !viewportOnly, timeout: 5000 });
  return evidence;
}
async function check(config, id, group, expected, procedure, observed, verify, p, capture = false) {
  const result = { config, id, group, expected, procedure, status: 'Fail' };
  try {
    result.actual = await observed();
    verify(result.actual);
    result.status = 'Pass';
  } catch (error) {
    result.error = error.message.slice(0, 1400);
    if (result.actual === undefined) result.actual = 'Observation interrupted. See execution error.';
  }
  if (capture || result.status === 'Fail') {
    try { result.evidence = await screenshot(p, group, `${config}-${id}`, group === 'compatibility'); }
    catch (error) { result.screenshotError = error.message; }
  }
  run.cases.push(result);
  console.log(`${config} ${id} ${result.status} ${JSON.stringify(result.actual)}`);
}
const equal = expected => actual => assert.deepEqual(actual, expected);
const includes = expected => actual => assert.ok(actual.includes(expected), JSON.stringify(actual));
const today = () => {
  const now = new Date();
  return [now.getFullYear(), String(now.getMonth() + 1).padStart(2, '0'), String(now.getDate()).padStart(2, '0')].join('-');
};
const layout = p => p.evaluate(() => ({
  innerWidth, documentWidth: document.documentElement.scrollWidth,
  viewportMeta: document.querySelector('meta[name=viewport]')?.content ?? null,
  horizontalScroll: document.documentElement.scrollWidth > innerWidth,
}));

async function workflows(p, config, user) {
  const test = (id, expected, steps, observed, verify, capture) =>
    check(config, id, 'gui', expected, steps, observed, verify, p, capture);
  await test('G01', 'Registration opens My Tasks for the new user.', 'From Log in click Register, enter a unique username and valid password, then submit.', async () => {
    await p.goto('/login');
    await link(p, 'Register').click();
    await credentials(p, user);
    await submit(p, button(p, 'Register'), '/');
    return [await text(p.locator('h1')), await text(p.locator('.nav-user'))];
  }, equal(['My Tasks', user]));
  await test('G02', 'Incorrect credentials are rejected with a readable error.', 'Log out, enter the registered username and a wrong password, then click Log in.', async () => {
    await link(p, 'Log out').click();
    await credentials(p, user, 'Incorrect123!');
    await button(p, 'Log in').click();
    return await text(p.locator('.error'));
  }, equal('Invalid username or password.'), deviceMode || config === 'chromium-desktop');
  await test('G03', 'Valid credentials restore the session and open My Tasks.', 'Enter the registered username and correct password and submit.', async () => {
    await credentials(p, user);
    await submit(p, button(p, 'Log in'), '/');
    return await text(p.locator('h1'));
  }, equal('My Tasks'));
  await test('G04', 'New task appears with its title, category and date.', 'Click + New Task, fill title, description, Work and 2099-04-10, then click Create Task.', async () => {
    await link(p, '+ New Task').click();
    await taskForm(p, 'Alpha planning');
    await submit(p, button(p, 'Create Task'), '/');
    return await row(p, 'Alpha planning').locator('td').allInnerTexts();
  }, actual => { for (const value of ['Alpha planning', 'Work', '2099-04-10', 'Upcoming']) includes(value)(actual); }, deviceMode || config === 'chromium-desktop');
  await test('G05', 'Edit form is prefilled and saves the updated title, category, date and description.', 'Click Edit for Alpha planning, inspect prefill, replace all four fields and save, then reopen Edit.', async () => {
    const values = () => Promise.all(['title', 'description', 'category_id', 'due_date'].map(name => field(p, name).inputValue()));
    await link(row(p, 'Alpha planning'), 'Edit').click();
    const before = await values();
    await taskForm(p, 'Alpha revised', 'Study', '2099-04-12');
    await field(p, 'description').fill('Updated description');
    await submit(p, button(p, 'Save Changes'), '/');
    const displayed = await row(p, 'Alpha revised').locator('td').allInnerTexts();
    await link(row(p, 'Alpha revised'), 'Edit').click();
    const after = await values();
    await link(p, 'Cancel').click();
    return { before, displayed, after };
  }, actual => {
    assert.deepEqual(actual.before, ['Alpha planning', 'Week 3 fixture description', '1', '2099-04-10']);
    assert.deepEqual(actual.after, ['Alpha revised', 'Updated description', '3', '2099-04-12']);
    includes('Study')(actual.displayed);
  });
  await test('G06', 'Completion can be toggled on, off and on again.', 'Activate the Alpha revised completion button three times and check each badge.', async () => {
    const states = [];
    for (const icon of ['○', '✓', '○']) {
      await Promise.all([p.waitForNavigation(), button(row(p, 'Alpha revised'), icon).click()]);
      states.push(await text(row(p, 'Alpha revised').locator('.badge')));
    }
    return states;
  }, equal(['Done', 'Upcoming', 'Done']));
  await test('G07', 'Title search matches a substring and gives a useful empty result.', 'Create Beta errands under Personal. Search for revised, then for missing-title.', async () => {
    await create(p, 'Beta errands', 'Personal');
    const results = [];
    for (const query of ['revised', 'missing-title']) {
      await field(p, 'q').fill(query);
      await Promise.all([p.waitForNavigation(), button(p, 'Filter').click()]);
      results.push(await p.locator('tbody tr td.title-cell, tbody td.empty').allInnerTexts());
    }
    return results;
  }, equal([['Alpha revised'], ['No tasks match your filters.']]));
  await test('G08', 'Category, open/done status and combined criteria select the expected tasks.', 'Clear search, select Study then Open then Done. Reset category and select Open.', async () => {
    await p.goto('/');
    const results = [];
    for (const [name, value] of [['category', 'Study'], ['status', 'open'], ['status', 'done'], ['category', ''], ['status', 'open']]) {
      await filter(p, name, value);
      results.push(await p.locator('.title-cell').allInnerTexts());
    }
    return results;
  }, equal([['Alpha revised'], [], ['Alpha revised'], ['Alpha revised'], ['Beta errands']]));
  await test('G09', 'Dashboard counters match 2 total, 1 open and 1 recently completed. Tasks returns to the list.', 'Click Dashboard, read all five counters, then use Tasks in the navigation.', async () => {
    await link(p, 'Dashboard').click();
    const counters = await p.locator('.stat-value').allInnerTexts();
    await link(p, 'Tasks').click();
    return [counters, await text(p.locator('h1'))];
  }, equal([['2', '1', '0', '0', '1'], 'My Tasks']));
  await test('G10', 'Cancelling preserves the task and confirming removes it after reload.', 'Click Delete for Beta errands, dismiss its dialog, then click Delete again and accept.', async () => {
    const remove = button(row(p, 'Beta errands'), 'Delete');
    let message;
    p.once('dialog', async dialog => { message = dialog.message(); await dialog.dismiss(); });
    await remove.click();
    const retained = await row(p, 'Beta errands').count();
    p.once('dialog', dialog => dialog.accept());
    await Promise.all([p.waitForNavigation(), remove.click()]);
    await p.reload();
    return [message, retained, await row(p, 'Beta errands').count(), await row(p, 'Alpha revised').count()];
  }, equal(['Delete this task?', 1, 0, 1]));
  await test('G11', 'Logout opens Log in and a fresh dashboard request redirects there.', 'Click Log out, then request /dashboard in the same browser context.', async () => {
    await link(p, 'Log out').click();
    const initial = new URL(p.url()).pathname;
    await p.goto('/dashboard');
    return [initial, new URL(p.url()).pathname];
  }, equal(['/login', '/login']));
}

async function detail(p, config, user) {
  const test = (id, group, expected, steps, observed, verify, capture) =>
    check(config, id, group, expected, steps, observed, verify, p, capture);
  await test('G12', 'gui', 'A blank username is blocked by required-field validation.', 'Open Register, fill only Password, submit.', async () => {
    await p.goto('/register');
    await field(p, 'password').fill(password);
    await button(p, 'Register').click();
    return field(p, 'username').evaluate(el => ({ missing: el.validity.valueMissing, message: el.validationMessage }));
  }, a => { assert.ok(a.missing && a.message); });
  await test('G13', 'gui', 'Invalid username and seven-character password produce the relevant messages.', 'Submit ab with a valid password, then use a valid username with 1234567.', async () => {
    const messages = [];
    for (const [name, secret] of [['ab', password], [user, '1234567']]) {
      await credentials(p, name, secret);
      await button(p, 'Register').click();
      messages.push(await text(p.locator('.error')));
    }
    return messages;
  }, equal(['Username must be 3-20 characters (letters, numbers, underscore).', 'Password must be at least 8 characters.']));
  await test('G14', 'gui', 'An eight-character password meets the displayed minimum.', 'Register a unique account using exactly 12345678.', async () => {
    await credentials(p, user, '12345678');
    await button(p, 'Register').click();
    return [await text(p.locator('h1')), await p.locator('.error').allInnerTexts()];
  }, equal(['My Tasks', []]));
  await register(p, user + '_detail');
  await test('G15', 'gui', 'An empty title is blocked by required-field validation.', 'Open New Task, leave Title empty and click Create Task.', async () => {
    await p.goto('/tasks/new');
    await button(p, 'Create Task').click();
    return field(p, 'title').evaluate(el => ({ missing: el.validity.valueMissing, message: el.validationMessage }));
  }, a => { assert.ok(a.missing && a.message); });
  for (const [id, form] of [['G16', 'Create Task'], ['G17', 'Save Changes']]) {
    await test(id, 'gui', 'Spaces-only title is rejected with feedback.', `Enter three spaces into Title and click ${form}.`, async () => {
      if (form === 'Save Changes') {
        await create(p, 'Editable task');
        await link(row(p, 'Editable task'), 'Edit').click();
      } else await p.goto('/tasks/new');
      await field(p, 'title').fill('   ');
      await button(p, form).click();
      return { heading: await text(p.locator('h1')), errors: await p.locator('.error').allInnerTexts(),
        blankRows: await p.locator('.title-cell').evaluateAll(cells => cells.filter(cell => !cell.textContent.trim()).length) };
    }, a => { assert.ok(a.errors.length && a.heading !== 'My Tasks'); });
  }
  await test('G18', 'gui', 'A task due today shows Due Today.', 'Create a Work task with today’s UTC date and read its badge.', async () => {
    await create(p, 'Due today sample', 'Work', today());
    return await text(row(p, 'Due today sample').locator('.badge'));
  }, equal('Due Today'));
  await test('G19', 'gui', 'Tasks and Dashboard use consistent navigation and page headings.', 'Compare nav link text and computed nav, background and heading styling on Tasks and Dashboard.', async () => {
    const audit = () => p.evaluate(() => ({
      nav: [...document.querySelectorAll('nav a')].map(a => a.textContent),
      navColor: getComputedStyle(document.querySelector('nav')).backgroundColor,
      background: getComputedStyle(document.body).backgroundColor,
      headingSize: getComputedStyle(document.querySelector('h1')).fontSize,
    }));
    const list = await audit();
    await link(p, 'Dashboard').click();
    return [list, await audit()];
  }, ([list, dashboard]) => assert.deepEqual(list, dashboard), true);
  await test('U01', 'usability', 'An empty task list gives a first-use explanation and visible creation action.', 'Register a fresh user and inspect the empty state.', async () => {
    await register(p, user + '_empty');
    return [await text(p.locator('.empty')), await link(p, '+ New Task').isVisible()];
  }, equal(['No tasks yet.', true]), true);
  await test('U02', 'usability', 'Creating a task gives explicit confirmation plus a visible new row.', 'Create Feedback sample and inspect the task list for a success message.', async () => {
    await create(p, 'Feedback sample');
    return [await row(p, 'Feedback sample').count(), await p.getByText(/task created|task saved/i).count()];
  }, equal([1, 1]), true);
  await test('U03', 'usability', 'Navigation identifies the active location beyond the page heading.', 'Click Dashboard and inspect the active nav link for aria-current or distinctive styling.', async () => {
    await link(p, 'Dashboard').click();
    return p.evaluate(() => {
      const items = [...document.querySelectorAll('.nav-links a')];
      return items.map(a => [a.textContent, a.getAttribute('aria-current'), getComputedStyle(a).fontWeight,
        getComputedStyle(a).textDecorationLine, getComputedStyle(a).color]);
    });
  }, a => assert.ok(a[1][1] === 'page' || JSON.stringify(a[0].slice(2)) !== JSON.stringify(a[1].slice(2))));
}

async function accessibility(p, config, user) {
  await p.context().clearCookies();
  const test = (id, expected, steps, observed, verify, capture) =>
    check(config, id, 'accessibility', expected, steps, observed, verify, p, capture);
  const stops = [
    ['login', () => p.goto('/login')],
    ['register', () => p.goto('/register')],
    ['empty-tasks', () => register(p, user)],
    ['populated-tasks', async () => {
      await create(p, 'Accessibility sample');
      await Promise.all([p.waitForNavigation(), button(row(p, 'Accessibility sample'), '○').click()]);
    }],
    ['dashboard', () => p.goto('/dashboard')],
    ['new-task', () => p.goto('/tasks/new')],
    ['edit-task', async () => { await p.goto('/'); await link(row(p, 'Accessibility sample'), 'Edit').click(); }],
  ];
  for (const [pageName, open] of stops) {
    await test(`A-axe-${pageName}`, 'Zero violations in the selected WCAG A/AA rules.', `Open ${pageName} and scan the rendered DOM.`, async () => {
      await open();
      await p.addScriptTag({ content: axe.source });
      const scan = await p.evaluate(() => window.axe.run({
        runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] },
      }));
      fs.writeFileSync(path.join(root, 'logs', `axe-${pageName}.json`), JSON.stringify(scan, null, 2));
      return { violations: scan.violations.map(v => ({ rule: v.id, nodes: v.nodes.length })),
        incomplete: scan.incomplete.map(v => v.id) };
    }, a => assert.equal(a.violations.length, 0), ['login', 'populated-tasks', 'new-task'].includes(pageName));
  }
  await p.context().clearCookies();
  await test('A08', 'Keyboard users can traverse Log in in order, reverse direction and activate Register.', 'Navigate to Log in, press Tab five times, Shift+Tab once, Tab then Enter.', async () => {
    await p.goto('/login');
    const moves = [];
    for (const key of ['Tab', 'Tab', 'Tab', 'Tab', 'Tab', 'Shift+Tab', 'Tab']) {
      await p.keyboard.press(key);
      moves.push(await p.evaluate(() => document.activeElement.name || document.activeElement.textContent.trim()));
    }
    await p.keyboard.press('Enter');
    await p.waitForURL('**/register');
    return moves;
  }, equal(['PyTodo Pro', 'username', 'password', 'Log in', 'Register', 'Log in', 'Register']));
  await test('A09', 'Focused login input has a detectable focus outline.', 'Open Log in and Tab twice. Measure focus-visible and outline and capture the focused form.', async () => {
    await p.goto('/login');
    await p.keyboard.press('Tab');
    await p.keyboard.press('Tab');
    return p.evaluate(() => {
      const el = document.activeElement;
      const style = getComputedStyle(el);
      return { field: el.name, visible: el.matches(':focus-visible'), style: style.outlineStyle, width: style.outlineWidth, color: style.outlineColor };
    });
  }, a => { assert.ok(a.field === 'username' && a.visible && a.style !== 'none' && parseFloat(a.width) > 0); }, true);
  await p.goto('/login');
  await credentials(p, user);
  await submit(p, button(p, 'Log in'), '/');
  await test('A10', 'Pages expose title, English language, H1, nav and main landmark.', 'Open Tasks, inspect semantic elements plus the task table headers.', async () => {
    await p.goto('/');
    return p.evaluate(() => ({
      title: document.title, lang: document.documentElement.lang, headings: document.querySelectorAll('h1').length,
      nav: document.querySelectorAll('nav').length, main: document.querySelectorAll('main, [role=main]').length,
      headers: [...document.querySelectorAll('th')].map(el => el.textContent.trim()),
    }));
  }, a => { assert.ok(a.title && a.lang === 'en' && a.headings === 1 && a.nav === 1 && a.main === 1); });
  await test('A11', 'At a 320 CSS px layout, navigation content fits the viewport.', 'Set desktop context viewport to 320 × 800, open Tasks and measure nav content and document widths.', async () => {
    await p.setViewportSize({ width: 320, height: 800 });
    await p.goto('/');
    return { ...await layout(p), navRight: await p.locator('.nav-links').evaluate(el => Math.round(el.getBoundingClientRect().right)) };
  }, a => assert.ok(a.navRight <= a.innerWidth), true);
  await test('A12', 'At 200% of the default root font size, task navigation and controls remain within the available page width.', 'Set viewport to 768 × 1024 and root font size to 200%. Inspect task list and new task form.', async () => {
    await p.setViewportSize({ width: 768, height: 1024 });
    const measures = [];
    for (const location of ['/', '/tasks/new']) {
      await p.goto(location);
      await p.addStyleTag({ content: 'html { font-size: 200%; }' });
      measures.push({ location, ...await layout(p),
        rootFont: await p.locator('html').evaluate(el => getComputedStyle(el).fontSize),
        offscreen: await p.locator('nav a, form button, form input, form select, form textarea, .btn-secondary, .btn').evaluateAll(
          elements => elements.filter(el => el.getBoundingClientRect().right > innerWidth).map(el => el.textContent.trim())) });
    }
    await screenshot(p, 'accessibility', config + '-A12-form');
    await p.goto('/');
    await p.addStyleTag({ content: 'html { font-size: 200%; }' });
    return measures;
  }, a => assert.ok(a.every(item => !item.horizontalScroll && !item.offscreen.length)), true);
  await test('A13', 'Task status toggle name identifies the action and task.', 'Restore desktop size, open Tasks and inspect the completion button’s accessible name and ARIA state.', async () => {
    await p.setViewportSize({ width: 1440, height: 900 });
    await p.goto('/');
    return await p.locator('.check-btn').ariaSnapshot();
  }, a => assert.match(a, /mark|reopen|complete/i));
}

async function compatibility(p, config, viewport, user) {
  await register(p, user);
  await create(p, 'Mobile layout sample');
  await check(config, 'C01', 'compatibility', 'Task list and navigation fit the configured CSS viewport.',
    'Open a populated Tasks page, measure document width and compare actual layout viewport to configured width.', async () => ({
      ...await layout(p), configuredWidth: viewport.width, navRight: await p.locator('.nav-links').evaluate(el => Math.round(el.getBoundingClientRect().right)),
    }), a => { assert.equal(a.innerWidth, viewport.width); assert.equal(a.horizontalScroll, false); }, p, true);
  await check(config, 'C02', 'compatibility', 'Dashboard cards stay within the configured CSS viewport.',
    'Open Dashboard and measure width and visibility of all five cards.', async () => {
      await link(p, 'Dashboard').click();
      return { ...await layout(p), cards: await p.locator('.stat-card').count() };
    }, a => { assert.equal(a.cards, 5); assert.equal(a.innerWidth, viewport.width); assert.equal(a.horizontalScroll, false); }, p,
  deviceMode || viewport.name === 'mobile');
}

async function main() {
  let ready = false;
  for (let attempt = 0; attempt < 60 && !ready; attempt++) {
    if (startupError || server.exitCode !== null) throw startupError || Error('Flask stopped during startup');
    try { ready = (await fetch(baseURL + '/login')).ok; }
    catch { await new Promise(resolve => setTimeout(resolve, 200)); }
  }
  if (!ready) throw Error('Flask readiness check timed out');
  const engines = { chromium, firefox, webkit };
  for (const [engine, launcher] of Object.entries(engines)) {
    const profiles = deviceMode
      ? deviceProfiles.filter(profile => profile.engine === engine).flatMap(({ descriptor }) =>
        ['portrait', 'landscape'].map(orientation => {
          const name = descriptor + (orientation === 'landscape' ? ' landscape' : '');
          const { defaultBrowserType, ...emulation } = devices[name];
          const config = descriptor.toLowerCase().replaceAll(' ', '-') + '-' + orientation;
          return { config, descriptor: name, orientation, emulation };
        }))
      : viewports.map(viewport => ({
        config: engine + '-' + viewport.name,
        viewportName: viewport.name,
        emulation: {
          viewport: { width: viewport.width, height: viewport.height },
          isMobile: viewport.mobile && engine !== 'firefox',
          hasTouch: viewport.mobile,
          deviceScaleFactor: 1,
        },
      }));
    if (!profiles.length) continue;
    let browser;
    let launchError;
    try { browser = await launcher.launch(); }
    catch (error) { launchError = error.message; }
    try {
      for (const [index, profile] of profiles.entries()) {
        const { config, descriptor, orientation, emulation, viewportName } = profile;
        const options = { baseURL, ...emulation, locale: 'en-US', timezoneId: 'UTC' };
        const entry = { config, engine, descriptor, orientation, version: browser?.version(), options, launchError };
        run.configurations.push(entry);
        if (!browser) { console.log(config + ' Not Run ' + launchError); continue; }
        const context = await browser.newContext(options);
        try {
          const p = await context.newPage();
          p.setDefaultTimeout(4500);
          p.setDefaultNavigationTimeout(6500);
          p.on('pageerror', error => console.error(config, 'pageerror', error.message));
          entry.userAgent = await p.evaluate(() => navigator.userAgent);
          const user = deviceMode ? `qa_${engine}_d${index + 1}` : 'qa_' + config.replaceAll('-', '_');
          await workflows(p, config, user);
          await compatibility(p, config, { ...options.viewport, name: viewportName }, user + 'c');
          if (config === 'chromium-desktop') {
            await detail(p, config, 'qa_chromium');
            await accessibility(p, config, 'qa_accessibility');
          }
        } catch (error) {
          entry.executionError = error.stack;
          console.error(config, error);
        } finally { await context.close(); }
      }
    } finally { await browser?.close(); }
  }
}

main().catch(error => {
  run.fatal = error.stack;
  console.error(error);
}).finally(() => {
  server.kill();
  run.finished = new Date().toISOString();
  fs.writeFileSync(logName('results.json'), JSON.stringify(run, null, 2));
  if (run.fatal || run.configurations.some(c => c.launchError || c.executionError) || run.cases.some(c => c.status === 'Fail')) process.exitCode = 1;
});
