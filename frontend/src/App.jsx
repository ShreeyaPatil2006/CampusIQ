import React, { useEffect, useMemo, useState } from 'react'
import { ArrowRight, BookOpen, BrainCircuit, Building2, CalendarDays, CheckCircle2, ChevronRight, GraduationCap, Menu, MessageCircle, Search, Send, ShieldCheck, Sparkles, X, Clock3, Users, Library, BriefcaseBusiness, Landmark, LogIn, Plus, Trash2, Pencil, Network, LogOut } from 'lucide-react'

const API = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'
const nav = ['Home', 'About', 'Academics', 'Admissions', 'Student Resources', 'Notices', 'Contact']
const quick = ['What is the minimum attendance requirement?', 'How do I apply for admission?', 'How can I apply for a scholarship?', 'Tell me about placements']

async function api(path, options={}) {
  const res = await fetch(`${API}${path}`, { headers: {'Content-Type':'application/json', ...(options.headers||{})}, ...options })
  const data = await res.json().catch(()=>({}))
  if (!res.ok) throw new Error(data.error || 'Something went wrong')
  return data
}

function ChatWidget() {
  const [open,setOpen]=useState(false), [text,setText]=useState(''), [busy,setBusy]=useState(false)
  const [session,setSession]=useState(null)
  const [messages,setMessages]=useState([{role:'assistant',content:"Hi! I'm CampusIQ, your college information assistant. Ask me about admissions, academics, attendance, examinations, scholarships or campus facilities."}])
  const send = async (value=text) => {
    const q=value.trim(); if(!q||busy)return
    setMessages(m=>[...m,{role:'user',content:q}]); setText(''); setBusy(true)
    try {
      const data=await api('/chat',{method:'POST',body:JSON.stringify({message:q,session_id:session})})
      setSession(data.session_id)
      setMessages(m=>[...m,{role:'assistant',content:data.answer,meta:data}])
    } catch(e) { setMessages(m=>[...m,{role:'assistant',content:`I couldn't reach the assistant service. Please check that the backend is running. (${e.message})`}]) }
    finally {setBusy(false)}
  }
  return <>
    <button className="chat-fab" onClick={()=>setOpen(!open)} aria-label="Open AI assistant">{open?<X/>:<MessageCircle/>}<span className="fab-pulse"/></button>
    {open&&<section className="chat-panel">
      <header className="chat-head"><div className="bot-avatar"><Sparkles size={19}/></div><div><b>CampusIQ Assistant</b><small><i/> Online · College knowledge base</small></div><button className="icon-btn light" onClick={()=>setOpen(false)}><X size={18}/></button></header>
      <div className="chat-messages">
        {messages.map((m,i)=><div key={i} className={`message ${m.role}`}><div className="bubble">{m.content}</div>{m.meta?.sources?.length>0&&<div className="sources"><b>Knowledge sources</b>{m.meta.sources.map((s,j)=><span key={j}>{s.category}: {s.question}</span>)}<small>Answer mode: {m.meta.mode}</small></div>}</div>)}
        {busy&&<div className="message assistant"><div className="bubble typing"><span/><span/><span/></div></div>}
      </div>
      {messages.length===1&&<div className="suggestions">{quick.map(q=><button key={q} onClick={()=>send(q)}>{q}<ChevronRight size={14}/></button>)}</div>}
      <form className="chat-input" onSubmit={e=>{e.preventDefault();send()}}><input value={text} onChange={e=>setText(e.target.value)} placeholder="Ask your college anything..." /><button disabled={busy||!text.trim()}><Send size={17}/></button></form>
      <div className="chat-foot">AI responses use the available demo knowledge base. Verify official policies.</div>
    </section>}
  </>
}

function Admin() {
  const [token,setToken]=useState(localStorage.getItem('campusiq_token')||'')
  const [email,setEmail]=useState('admin@campusiq.demo'),[password,setPassword]=useState('CampusIQ@123')
  const [faqs,setFaqs]=useState([]),[question,setQuestion]=useState(''),[answer,setAnswer]=useState(''),[category,setCategory]=useState('General'),[keywords,setKeywords]=useState('')
  const [notice,setNotice]=useState('')
  const auth={Authorization:`Bearer ${token}`}
  const load=async()=>{try{setFaqs(await api('/admin/faqs',{headers:auth}))}catch(e){setNotice(e.message);setToken('');localStorage.removeItem('campusiq_token')}}
  useEffect(()=>{if(token)load()},[token])
  const login=async e=>{e.preventDefault();try{const d=await api('/auth/login',{method:'POST',body:JSON.stringify({email,password})});setToken(d.token);localStorage.setItem('campusiq_token',d.token);setNotice('Signed in successfully')}catch(e){setNotice(e.message)}}
  const add=async e=>{e.preventDefault();try{await api('/admin/faqs',{method:'POST',headers:auth,body:JSON.stringify({question,answer,category,keywords})});setQuestion('');setAnswer('');setKeywords('');setNotice('FAQ added to the knowledge base');load()}catch(e){setNotice(e.message)}}
  const remove=async id=>{if(!confirm('Delete this knowledge-base entry?'))return;try{await api(`/admin/faqs/${id}`,{method:'DELETE',headers:auth});load()}catch(e){setNotice(e.message)}}
  if(!token)return <div className="admin-wrap"><form className="admin-login" onSubmit={login}><div className="bot-avatar"><ShieldCheck/></div><h2>Administrator sign in</h2><p>Manage CampusIQ knowledge and notices.</p><label>Email<input value={email} onChange={e=>setEmail(e.target.value)}/></label><label>Password<input type="password" value={password} onChange={e=>setPassword(e.target.value)}/></label><button className="btn primary">Sign in <ArrowRight size={16}/></button>{notice&&<small className="notice">{notice}</small>}<small>Demo credentials are documented in README. Change them before deployment.</small></form></div>
  return <div className="admin-wrap"><div className="admin-main"><div className="section-heading"><div><span className="eyebrow">CONTROL CENTER</span><h2>Knowledge base manager</h2><p>Add verified information that CampusIQ can retrieve.</p></div><button className="btn outline" onClick={()=>{setToken('');localStorage.removeItem('campusiq_token')}}><LogOut size={16}/> Sign out</button></div>
    <form className="admin-form" onSubmit={add}><h3><Plus size={18}/> Add knowledge entry</h3><label>Question<input required value={question} onChange={e=>setQuestion(e.target.value)} placeholder="e.g. What is the attendance policy?"/></label><label>Answer<textarea required rows="4" value={answer} onChange={e=>setAnswer(e.target.value)} placeholder="Enter verified college information..."/></label><div className="form-row"><label>Category<input value={category} onChange={e=>setCategory(e.target.value)}/></label><label>Keywords<input value={keywords} onChange={e=>setKeywords(e.target.value)} placeholder="attendance, lectures, exams"/></label></div><button className="btn primary">Save to knowledge base <ArrowRight size={16}/></button>{notice&&<small className="notice">{notice}</small>}</form>
    <div className="entries-head"><h3>Knowledge entries <span>{faqs.length}</span></h3></div><div className="entry-list">{faqs.map(f=><article className="entry" key={f.id}><div><span className="pill">{f.category}</span><b>{f.question}</b><p>{f.answer}</p></div><button className="icon-btn danger" onClick={()=>remove(f.id)} title="Delete"><Trash2 size={17}/></button></article>)}</div>
  </div></div>
}

export default function App(){
  const [page,setPage]=useState('Home'),[mobile,setMobile]=useState(false),[content,setContent]=useState(null),[loadError,setLoadError]=useState('')
  useEffect(()=>{api('/content').then(setContent).catch(e=>setLoadError(e.message))},[])
  const announcements=content?.announcements||[]
  const departments=content?.departments||[]
  const go=p=>{setPage(p);setMobile(false);window.scrollTo({top:0,behavior:'smooth'})}
  if(page==='Admin')return <><Header page={page} go={go}/><Admin/><ChatWidget/><Footer go={go}/></>
  return <><Header page={page} go={go} mobile={mobile} setMobile={setMobile}/>
    {page==='Home'&&<Home go={go} announcements={announcements} departments={departments}/>}
    {page==='About'&&<InfoPage eyebrow="OUR INSTITUTION" title="Education that moves ideas forward" text="Northstar Institute of Technology is a fictional demonstration institution used to showcase CampusIQ. Replace this section with your college's verified history, vision, mission and achievements." cards={['Learning by doing','Supportive student community','Industry-aware education']}/>}
    {page==='Academics'&&<Academics departments={departments}/>}
    {page==='Admissions'&&<Admissions/>}
    {page==='Student Resources'&&<Resources go={go}/>}
    {page==='Notices'&&<Notices items={announcements}/>}
    {page==='Contact'&&<Contact/>}
    {loadError&&<div className="api-warning">Backend connection: {loadError}. Start the Flask server to load live content and enable the assistant.</div>}
    <ChatWidget/><Footer go={go}/>
  </>
}

function Header({page,go,mobile,setMobile}){
  return <header className="site-header"><div className="nav-shell"><button className="brand" onClick={()=>go('Home')}><span className="brand-mark"><Landmark size={22}/></span><span>northstar<span className="brand-sub">INSTITUTE OF TECHNOLOGY</span></span></button><nav className={mobile?'nav-links show':'nav-links'}>{nav.map(n=><button key={n} className={page===n?'active':''} onClick={()=>go(n)}>{n}</button>)}<button className="admin-link" onClick={()=>go('Admin')}><LogIn size={15}/> Admin</button></nav><button className="menu-btn" onClick={()=>setMobile(!mobile)}><Menu/></button></div></header>
}
function Home({go,announcements,departments}){
 return <><section className="hero"><div className="hero-grid"><div className="hero-copy"><div className="eyebrow"><span/> YOUR FUTURE STARTS HERE</div><h1>Think bigger.<br/><em>Build what's next.</em></h1><p>A place to explore ideas, develop skills and turn ambition into meaningful impact. Discover programmes, campus life and student support.</p><div className="hero-actions"><button className="btn primary" onClick={()=>go('Admissions')}>Explore admissions <ArrowRight size={17}/></button><button className="btn ghost" onClick={()=>go('Academics')}>Explore academics</button></div><div className="hero-proof"><div className="avatar-stack"><span>N</span><span>I</span><span>T</span></div><small><b>One connected campus</b><br/>Knowledge, opportunity and community</small></div></div><div className="hero-visual"><div className="visual-orbit orbit-one"/><div className="visual-orbit orbit-two"/><div className="campus-art"><div className="sun"/><div className="building"><div className="roof"/><div className="columns"><i/><i/><i/><i/><i/></div><div className="steps"/></div><div className="tree tree-a"/><div className="tree tree-b"/></div><div className="float-card card-top"><span className="float-icon"><GraduationCap size={19}/></span><span><b>Learn with purpose</b><small>Explore your potential</small></span></div><div className="float-card card-bottom"><span className="float-icon aqua"><Sparkles size={18}/></span><span><b>CampusIQ AI</b><small>Answers, whenever you need</small></span></div><div className="visual-label">NORTHSTAR · EST. FOR TOMORROW</div></div></div></section>
 <section className="trust-strip"><div><b>01</b><span>Academic pathways</span></div><div><b>02</b><span>Student-first support</span></div><div><b>03</b><span>Ideas into action</span></div><div><b>04</b><span>Connected community</span></div></section>
 <section className="section"><div className="section-heading"><div><span className="eyebrow">DISCOVER NORTHSTAR</span><h2>Room to find your direction.</h2><p>Explore the people, programmes and resources that make campus life happen.</p></div><button className="text-link" onClick={()=>go('About')}>About the institute <ArrowRight size={16}/></button></div><div className="feature-grid"><Feature icon={<BookOpen/>} num="01" title="Academic excellence" text="Explore learning pathways and academic resources." go={()=>go('Academics')}/><Feature icon={<Users/>} num="02" title="Student community" text="Find support, activities and opportunities to grow." go={()=>go('Student Resources')}/><Feature icon={<BriefcaseBusiness/>} num="03" title="Career pathways" text="Discover internship and placement guidance." go={()=>go('Student Resources')}/></div></section>
 <section className="department-section"><div className="section-heading"><div><span className="eyebrow">FIND YOUR FIELD</span><h2>Explore our departments.</h2><p>Sample academic departments shown for demonstration.</p></div><button className="text-link" onClick={()=>go('Academics')}>All academics <ArrowRight size={16}/></button></div><div className="department-grid">{departments.slice(0,4).map((d,i)=><div className="department-card" key={d.id}><span className="dept-number">0{i+1}</span><h3>{d.name}</h3><p>{d.description}</p><button onClick={()=>go('Academics')}>Discover department <ArrowRight size={15}/></button></div>)}</div></section>
 <section className="ai-banner"><div className="ai-symbol"><BrainCircuit size={34}/><span/></div><div><span className="eyebrow">MEET YOUR DIGITAL CAMPUS GUIDE</span><h2>Questions? Start with CampusIQ.</h2><p>Ask in your own words. Get guided answers from the college knowledge base.</p></div><button className="btn light-btn" onClick={()=>document.querySelector('.chat-fab')?.click()}>Ask CampusIQ <MessageCircle size={17}/></button></section>
 <section className="section news-section"><div className="section-heading"><div><span className="eyebrow">CAMPUS UPDATES</span><h2>What's happening.</h2></div><button className="text-link" onClick={()=>go('Notices')}>View all notices <ArrowRight size={16}/></button></div><div className="news-grid">{announcements.slice(0,3).map(a=><article className="news-card" key={a.id}><span className="pill">{a.tag}</span><small><CalendarDays size={14}/>{a.date}</small><h3>{a.title}</h3><p>{a.body}</p><button onClick={()=>go('Notices')}>Read notice <ArrowRight size={15}/></button></article>)}</div></section></>
}
function Feature({icon,num,title,text,go}){return <article className="feature-card"><div className="feature-top">{icon}<span>{num}</span></div><h3>{title}</h3><p>{text}</p><button onClick={go}>Explore <ArrowRight size={15}/></button></article>}
function PageHero({eyebrow,title,text}){return <section className="page-hero"><span className="eyebrow">{eyebrow}</span><h1>{title}</h1><p>{text}</p></section>}
function InfoPage({eyebrow,title,text,cards}){return <><PageHero eyebrow={eyebrow} title={title} text={text}/><section className="section"><div className="simple-grid">{cards.map((c,i)=><div className="simple-card" key={c}><span>0{i+1}</span><h3>{c}</h3><p>Replace this sample copy with verified institutional information.</p></div>)}</div></section></>}
function Academics({departments}){return <><PageHero eyebrow="ACADEMIC PATHWAYS" title="Find the subject that moves you." text="Explore sample programmes and departments. Confirm current offerings and eligibility with the official admissions office."/><section className="section"><div className="department-grid">{departments.map((d,i)=><article className="department-card" key={d.id}><span className="dept-number">0{i+1}</span><h3>{d.name}</h3><p>{d.description}</p><div className="program-line"><GraduationCap size={16}/>{d.programs}</div></article>)}</div></section></>}
function Admissions(){return <><PageHero eyebrow="START YOUR JOURNEY" title="Your next chapter begins here." text="A simple overview of a typical application journey. Programme-specific requirements and dates must be confirmed with the official admissions office."/><section className="section"><div className="steps-grid">{[['01','Explore programmes','Review courses, eligibility and programme details.'],['02','Prepare documents','Gather marksheets, identity documents and any programme-specific certificates.'],['03','Submit application','Complete the official application process and retain your acknowledgement.'],['04','Confirm admission','Follow official communication for verification, fee payment and enrolment.']].map(x=><div className="step-card" key={x[0]}><b>{x[0]}</b><h3>{x[1]}</h3><p>{x[2]}</p></div>)}</div><div className="notice-box"><ShieldCheck/><div><b>Important</b><p>This demo portal does not publish official admission dates, fees or eligibility rules. Always verify these with your institution.</p></div></div></section></>}
function Resources({go}){const items=[['Attendance & exams','Understand academic processes and assessment guidance.',BookOpen],['Scholarships','Explore financial-aid guidance and application basics.',Landmark],['Placements & internships','Find career preparation and opportunity resources.',BriefcaseBusiness],['Library & campus','Learn about study spaces and student facilities.',Library]];return <><PageHero eyebrow="HERE TO HELP" title="Your student toolkit." text="Find guidance for common student questions, all in one place."/><section className="section"><div className="resource-grid">{items.map(([t,d,I])=><article className="resource-card" key={t}><I/><h3>{t}</h3><p>{d}</p><button className="text-link" onClick={()=>document.querySelector('.chat-fab')?.click()}>Ask CampusIQ <ArrowRight size={15}/></button></article>)}</div></section></>}
function Notices({items}){return <><PageHero eyebrow="CAMPUS BULLETIN" title="The latest from campus." text="Announcements and student updates. Demo entries are illustrative; replace them with approved notices."/><section className="section"><div className="notice-list">{items.map(a=><article className="notice-item" key={a.id}><div className="notice-date"><CalendarDays/><span>{a.date}</span></div><div><span className="pill">{a.tag}</span><h3>{a.title}</h3><p>{a.body}</p></div></article>)}</div></section></>}
function Contact(){return <><PageHero eyebrow="GET IN TOUCH" title="We're here to point you in the right direction." text="This demonstration portal uses placeholder contact details. Replace them with verified college contact information."/><section className="section"><div className="contact-grid"><div className="contact-card"><Building2/><h3>Visit the campus</h3><p>Northstar Institute of Technology<br/>Demo Campus, India</p></div><div className="contact-card"><MessageCircle/><h3>General enquiries</h3><p>Use your institution's official contact channel. No verified email is configured in this demo.</p></div><div className="contact-card"><Clock3/><h3>Office hours</h3><p>Refer to the official college website for current office hours.</p></div></div></section></>}
function Footer({go}){return <footer className="footer"><div className="footer-main"><div className="footer-brand"><div className="brand"><span className="brand-mark"><Landmark size={22}/></span><span>northstar<span className="brand-sub">INSTITUTE OF TECHNOLOGY</span></span></div><p>A demonstration college portal powered by an intelligent information assistant.</p></div><div><b>Explore</b>{['About','Academics','Admissions'].map(x=><button key={x} onClick={()=>go(x)}>{x}</button>)}</div><div><b>Student help</b>{['Student Resources','Notices','Contact'].map(x=><button key={x} onClick={()=>go(x)}>{x}</button>)}</div><div><b>CampusIQ</b><p>Ask questions in natural language and explore the knowledge base.</p><button onClick={()=>go('Admin')}>Administrator portal <ArrowRight size={14}/></button></div></div><div className="footer-bottom"><span>© 2026 Northstar Institute · CampusIQ demo</span><span>Demo content · Verify official information</span></div></footer>}
