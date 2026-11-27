const assert = require('node:assert/strict');
const { randomBytes } = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { spawn } = require('node:child_process');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '..');
const baseURL = 'http://127.0.0.1:51794';
const secret = randomBytes(18).toString('hex');
const run = { started: new Date().toISOString(), playwright: require('playwright/package.json').version,
  node: process.version, options: { baseURL, viewport: { width: 1440, height: 900 }, locale: 'en-US', timezoneId: 'UTC' },
  cases: [] };
const log = fs.openSync(path.join(root, 'logs/web-flask.log'), 'w');
const server = spawn(process.env.QA_PYTHON || 'python', ['-B', path.join(__dirname, 'server.py'), '51794'],
  { stdio: ['ignore', log, log], env: { ...process.env, TZ: 'UTC' } });
fs.closeSync(log);
let startupError;
server.on('error', error => { startupError = error; });

const field = (p, name) => p.locator(`[name="${name}"]`);
const button = (p, name) => p.getByRole('button', { name, exact: true });
const link = (p, name) => p.getByRole('link', { name, exact: true });
const title = p => p.locator('h1').innerText();
const rows = p => p.locator('.title-cell').allInnerTexts();
const row = (p, name) => p.locator('tbody tr').filter({ hasText: name });
const pathname = url => new URL(url).pathname;
const postAndLoad = (p, trigger) => Promise.all([p.waitForNavigation(), trigger()]);
const select = (p, key, value) => postAndLoad(p, () => field(p, key).selectOption(value));

async function credentials(p, username, password) {
  await field(p, 'username').fill(username);
  await field(p, 'password').fill(password);
}
async function register(p, user) {
  await p.goto('/register');
  await credentials(p, user, secret);
  await postAndLoad(p, () => button(p,'Register').click());
  assert.equal(pathname(p.url()), '/');
}
async function create(p, name, category = '1', due = '') {
  await p.goto('/tasks/new');
  await field(p, 'title').fill(name);
  await field(p, 'category_id').selectOption(category);
  if (due) await field(p, 'due_date').fill(due);
  await postAndLoad(p, () => button(p, 'Create Task').click());
}

function safePayload(data, contentType) {
  if (!data) return null;
  const payload = contentType.includes('json') ? JSON.parse(data) : Object.fromEntries(new URLSearchParams(data));
  if ('password' in payload) payload.password = `<redacted; length=${payload.password.length}>`;
  return payload;
}
function requestRecord(req) {
  const headers = req.headers();
  return { method: req.method(), url: req.url().slice(baseURL.length),
    headers: { 'content-type': headers['content-type'], accept: headers.accept },
    payload: safePayload(req.postData(), headers['content-type'] || '') };
}
async function api(result, p, method, url, payload, form = false) {
  const headers = { Accept: form ? 'text/html' : 'application/json' };
  if (payload) headers['Content-Type'] = form ? 'application/x-www-form-urlencoded' : 'application/json';
  const response = await p.request.fetch(url, { method, headers, maxRedirects: 0,
    ...(payload ? form ? { form: payload } : { data: payload } : {}) });
  const responseType = response.headers()['content-type'];
  const json = responseType.includes('application/json') ? await response.json() : null;
  const safe = payload ? { ...payload } : null;
  if (safe && 'password' in safe) safe.password = `<redacted; length=${safe.password.length}>`;
  const evidence = { method, url, headers, payload: safe, status: response.status(),
    location: response.headers().location, responseType, json };
  result.requests.push(evidence);
  return evidence;
}

const cases = [
  ['W01', 'Visitor redirects to login, valid registration signs in, valid login restores access after logout.',
    'Request Dashboard anonymously. Register, log out, log in and open Dashboard.',
    ['/login','My Tasks','/login','Dashboard'], async (p,id) => {
      await p.goto('/dashboard');
      const guest = pathname(p.url());
      await register(p,id);
      const registered = await title(p);
      await link(p,'Log out').click();
      const logout = pathname(p.url());
      await credentials(p,id,secret);
      await postAndLoad(p,()=>button(p,'Log in').click());
      await link(p,'Dashboard').click();
      return [guest,registered,logout,await title(p)];
    }],
  ['W02','Invalid username, short password and wrong login receive readable validation feedback.',
    'Submit a two-character username, then a seven-character password, then sign in with an incorrect password.',
    ['Username must be 3-20 characters (letters, numbers, underscore).','Password must be at least 8 characters.','Invalid username or password.'],
    async (p,id) => {
      const messages=[];
      await p.goto('/register');
      for (const [name,password] of [['ab',secret],[id,secret.slice(0,7)]]) {
        await credentials(p,name,password);
        await postAndLoad(p,()=>button(p,'Register').click());
        messages.push(await p.locator('.error').innerText());
      }
      await register(p,id);
      await link(p,'Log out').click();
      await credentials(p,id,randomBytes(10).toString('hex'));
      await postAndLoad(p,()=>button(p,'Log in').click());
      return [...messages,await p.locator('.error').innerText()];
    }],
  ['W03','Browser prevents required-field submission.',
    'On Register leave Username blank. On New Task leave Title blank. Click the submit controls and inspect validity and POST traffic.',
    [true,0,true,0], async (p,id,result) => {
      await p.goto('/register');
      await field(p,'password').fill(secret);
      await button(p,'Register').click();
      const reg = await field(p,'username').evaluate(el=>el.validity.valueMissing);
      const regPosts = result.requests.filter(x=>x.method==='POST').length;
      await register(p,id);
      await p.goto('/tasks/new');
      const before = result.requests.length;
      await button(p,'Create Task').click();
      return [reg,regPosts,await field(p,'title').evaluate(el=>el.validity.valueMissing),
        result.requests.slice(before).filter(x=>x.method==='POST').length];
    }],
  ['W04','Create, edit, complete, reopen and delete a task.',
    'Create an open task, edit its title, complete and reopen it, cancel deletion, then confirm deletion.',
    ['Revised','Done','Upcoming','Delete this task?',1,0], async (p,id) => {
      await register(p,id);
      await create(p,'Original','1','2099-04-10');
      await link(row(p,'Original'),'Edit').click();
      await field(p,'title').fill('Revised');
      await postAndLoad(p,()=>button(p,'Save Changes').click());
      const revised = (await rows(p))[0];
      const task = row(p,'Revised');
      await postAndLoad(p,()=>button(task,'○').click());
      const done = await task.locator('.badge').innerText();
      await postAndLoad(p,()=>button(task,'✓').click());
      const reopened = await task.locator('.badge').innerText();
      let prompt;
      p.once('dialog',async dialog=>{prompt=dialog.message();await dialog.dismiss();});
      await button(task,'Delete').click();
      const retained = await task.count();
      p.once('dialog',dialog=>dialog.accept());
      await postAndLoad(p,()=>button(task,'Delete').click());
      return [revised,done,reopened,prompt,retained,await task.count()];
    }],
  ['W05','Title search and combined category/status filters return only matching tasks.',
    'Create Work/Alpha plan and Personal/Alpha home, complete Alpha plan, search Alpha, then apply Work and Done.',
    [['Alpha home','Alpha plan'],['Alpha plan'],['Alpha plan']], async(p,id)=>{
      await register(p,id);
      await create(p,'Alpha plan','1');
      await postAndLoad(p,()=>button(row(p,'Alpha plan'),'○').click());
      await create(p,'Alpha home','2');
      await field(p,'q').fill('Alpha');
      await postAndLoad(p,()=>button(p,'Filter').click());
      const search=await rows(p);
      await select(p,'category','Work');
      const category=await rows(p);
      await select(p,'status','done');
      return [search,category,await rows(p)];
    }],
  ['W06','Dashboard counts task states and dates accurately and links back to Tasks.',
    'Create an overdue task, a task due tomorrow and a completed task, then review counters.',
    [['3','2','1','1','1'],'My Tasks'], async(p,id,result)=>{
      await register(p,id);
      const day = offset => new Date(Date.now()+offset*86400000).toISOString().slice(0,10);
      await create(p,'Overdue','1',day(-1));
      await create(p,'Tomorrow','1',day(1));
      await create(p,'Finished','2',day(5));
      await postAndLoad(p,()=>button(row(p,'Finished'),'○').click());
      await link(p,'Dashboard').click();
      const counters=await p.locator('.stat-value').allInnerTexts();
      result.extraEvidence = await capture(p,id+'-dashboard','web');
      await link(p,'Tasks').click();
      return [counters,await title(p)];
    }],
  ['W07','Registration accepts passwords at the advertised eight-character minimum.',
    'Submit a fresh username with an eight-character password.',
    ['My Tasks',[]], async(p,id)=>{
      await p.goto('/register');
      await credentials(p,id,secret.slice(0,8));
      await postAndLoad(p,()=>button(p,'Register').click());
      return [await title(p),await p.locator('.error').allInnerTexts()];
    }],
  ['W08','The web server rejects a missing title even without the browser required check.',
    'Sign in and submit a form request omitting Title. Inspect the resulting task list.',
    [true,0], async(p,id,result)=>{
      await register(p,id);
      const response = await api(result,p,'POST','/tasks/new',{description:'Missing title fixture'},true);
      await p.goto('/');
      return [[200,400,422].includes(response.status),(await rows(p)).length];
    }],
  ['I01','API registration and task creation are visible in the browser session.',
    'Register and create a Work task through the API in the browser context. Open My Tasks.',
    [201,201,'qa_i01',['API to UI'],'Work'], async(p,id,result)=>{
      const user=await api(result,p,'POST','/api/register',{username:id,password:secret});
      const task=await api(result,p,'POST','/api/tasks',{title:'API to UI',category_id:1});
      await p.goto('/');
      return [user.status,task.status,await p.locator('.nav-user').innerText(),await rows(p),
        await row(p,'API to UI').locator('td').nth(2).innerText()];
    }],
  ['I02','Web create and complete appear in API list and dashboard. API update and deletion appear in the UI.',
    'Create and complete UI to API in the browser. Read API list/dashboard, reopen and rename via API, reload, then delete through the API.',
    [200,'UI to API',true,200,1,200,'API revision','Upcoming',200,[]], async(p,id,result)=>{
      await register(p,id);
      await create(p,'UI to API','1','2099-04-10');
      await postAndLoad(p,()=>button(row(p,'UI to API'),'○').click());
      const listing=await api(result,p,'GET','/api/tasks');
      const dashboard=await api(result,p,'GET','/api/dashboard');
      const task=listing.json[0];
      const url='/api/tasks/'+task.id;
      const edit=await api(result,p,'PUT',url,{title:'API revision',done:false});
      await p.reload();
      const revised=(await rows(p))[0];
      const urgency=await row(p,'API revision').locator('.badge').innerText();
      result.extraEvidence=await capture(p,id+'-updated','comparison');
      const deleted=await api(result,p,'DELETE',url);
      await p.reload();
      return [listing.status,task.title,task.done,dashboard.status,dashboard.json.completed_this_week,
        edit.status,revised,urgency,deleted.status,await rows(p)];
    }],
  ['I03','Web and API task creation both reject a whitespace-only title.',
    'Enter three spaces in the web form, then send the same title in an API create request. Inspect the list and API error.',
    [400,'title is required',0], async(p,id,result)=>{
      await register(p,id);
      await create(p,'   ');
      const webRows=(await rows(p)).length;
      const response=await api(result,p,'POST','/api/tasks',{title:'   '});
      return [response.status,response.json.error,webRows];
    }],
  ['I04','Web logout clears the API session in the same browser context.',
    'Register through the web, query API tasks, log out through the web and query the API again.',
    [200,401,'authentication required','/login'], async(p,id,result)=>{
      await register(p,id);
      const before=await api(result,p,'GET','/api/tasks');
      await link(p,'Log out').click();
      const after=await api(result,p,'GET','/api/tasks');
      return [before.status,after.status,after.json.error,pathname(p.url())];
    }],
];

async function capture(p,id,category) {
  const relative=`screenshots/${category}/${id}.png`;
  const target=path.join(root,relative);
  fs.mkdirSync(path.dirname(target),{recursive:true});
  await p.screenshot({path:target,fullPage:true,timeout:5000});
  return relative;
}

async function main() {
  let ready=false;
  for (let i=0;i<50&&!ready;i++) {
    if (startupError || server.exitCode!==null) throw startupError || Error('Flask exited during startup');
    try { ready=(await fetch(baseURL+'/login')).ok; }
    catch { await new Promise(resolve=>setTimeout(resolve,200)); }
  }
  if (!ready) throw Error('Flask did not become ready');
  const browser=await chromium.launch();
  run.browser=browser.version();
  try {
    for (const [id,objective,steps,expected,execute] of cases) {
      const context=await browser.newContext(run.options);
      const p=await context.newPage();
      p.setDefaultTimeout(5000);
      const group=id.startsWith('I')?'comparison':'web';
      const result={id,group,objective,steps,expected,requests:[],status:'Fail'};
      p.on('response',response=>{
        const request=response.request();
        if (request.resourceType()==='document') {
          result.requests.push({...requestRecord(request),status:response.status(),
            location:response.headers().location,responseType:response.headers()['content-type']});
        }
      });
      try {
        result.actual=await execute(p,'qa_'+id.toLowerCase(),result);
        assert.deepEqual(result.actual,expected);
        result.status='Pass';
      } catch(error) {
        result.error=error.message.replaceAll(secret,'<redacted>');
      }
      try { result.evidence=await capture(p,id,group); }
      catch(error) { result.screenshotError=error.message; }
      run.cases.push(result);
      console.log(id,result.status,JSON.stringify(result.actual));
      await context.close();
    }
  } finally { await browser.close(); }
}
main().catch(error=>{run.fatal=error.message;console.error(error);}).finally(()=>{
  server.kill();
  run.finished=new Date().toISOString();
  fs.writeFileSync(path.join(root,'logs/web-results.json'),JSON.stringify(run,null,2));
  if (run.fatal || run.cases.some(c=>c.status==='Fail'||c.screenshotError)) process.exitCode=1;
});
