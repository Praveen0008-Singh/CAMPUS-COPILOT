import streamlit as st
from datetime import datetime
import uuid

st.set_page_config(
    page_title="Campus Copilot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- STATE ----------------
defaults = {
    "page": "Home",
    "complaints": [],
    "lost_found": [],
    "messages": [],
    "notice_filter": "All",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root{--bg:#060913;--line:rgba(148,163,184,.15);--text:#f8fafc;--muted:#94a3b8}
.stApp{background:radial-gradient(circle at 8% 5%,rgba(34,211,238,.10),transparent 24%),radial-gradient(circle at 92% 8%,rgba(139,92,246,.13),transparent 26%),#060913;color:var(--text);font-family:Inter,sans-serif}
#MainMenu,footer{visibility:hidden} header{background:transparent!important}
.block-container{max-width:1450px;padding-top:28px;padding-bottom:50px}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#080d18,#10192b);border-right:1px solid rgba(255,255,255,.07)}
section[data-testid="stSidebar"] *{color:#f8fafc!important}
.brand{padding:8px 4px 22px}.brand-title{font-size:24px;font-weight:800}.brand-sub{color:#8fa1bb!important;font-size:12px;margin-top:5px}
.nav-title{color:#64748b!important;font-size:10px;font-weight:800;letter-spacing:1.5px;margin:12px 0 8px}
div.stButton>button{width:100%;min-height:44px;border-radius:13px;border:1px solid rgba(148,163,184,.12);background:rgba(30,41,59,.55);color:#e2e8f0;font-weight:650;transition:all .25s ease}
div.stButton>button:hover{transform:translateY(-2px);border-color:rgba(56,189,248,.38);box-shadow:0 10px 30px rgba(0,0,0,.25)}
.primary-btn button{background:linear-gradient(135deg,#2563eb,#7c3aed)!important;border:none!important}
.hero{position:relative;min-height:360px;padding:48px;border-radius:32px;overflow:hidden;background:linear-gradient(135deg,rgba(15,23,42,.94),rgba(17,28,51,.72));border:1px solid var(--line);box-shadow:0 30px 90px rgba(0,0,0,.35);animation:pageIn .65s cubic-bezier(.2,.8,.2,1)}
.hero:before{content:"";position:absolute;width:520px;height:520px;right:-180px;top:-240px;border-radius:50%;background:radial-gradient(circle,rgba(34,211,238,.22),rgba(139,92,246,.08),transparent 68%);animation:glow 5s ease-in-out infinite}
.hero:after{content:"";position:absolute;inset:0;opacity:.28;pointer-events:none;background-image:linear-gradient(rgba(255,255,255,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px);background-size:42px 42px;transform:perspective(500px) rotateX(62deg) translateY(135px) scale(1.5)}
.hero-content{position:relative;z-index:5;max-width:650px}.badge{display:inline-flex;padding:8px 13px;border-radius:99px;color:#67e8f9;background:rgba(34,211,238,.08);border:1px solid rgba(34,211,238,.20);font-size:11px;font-weight:800;letter-spacing:.8px}
.hero h1{font-size:58px;line-height:1;margin:20px 0 15px;font-weight:800;letter-spacing:-2.5px;background:linear-gradient(90deg,#fff,#7dd3fc,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{color:#a8b5c8;font-size:16px;line-height:1.75;max-width:610px}
.orb{position:absolute;right:110px;top:78px;width:165px;height:165px;border-radius:50%;z-index:4;background:radial-gradient(circle at 32% 27%,#fff 0 5%,#67e8f9 9%,#38bdf8 22%,#2563eb 46%,#7c3aed 72%,#0f172a 100%);box-shadow:0 0 38px rgba(56,189,248,.52),0 0 100px rgba(139,92,246,.28);animation:float 4s ease-in-out infinite}
.orb:before,.orb:after{content:"";position:absolute;border-radius:50%;inset:-16px;border:1px solid rgba(103,232,249,.32)}
.orb:before{transform:rotateX(70deg);animation:orbit 5s linear infinite}.orb:after{inset:-29px;border-color:rgba(167,139,250,.25);transform:rotateY(70deg);animation:orbit2 7s linear infinite}
.section-title{font-size:27px;font-weight:800;margin:34px 0 16px;letter-spacing:-.7px}.muted{color:var(--muted)}
.card{padding:24px;border-radius:22px;background:linear-gradient(145deg,rgba(30,41,59,.78),rgba(15,23,42,.70));border:1px solid var(--line);min-height:175px;transition:transform .3s ease,border .3s ease,box-shadow .3s ease;animation:pageIn .55s ease both}
.card:hover{transform:translateY(-7px);border-color:rgba(56,189,248,.30);box-shadow:0 24px 55px rgba(0,0,0,.30)}
.icon{width:55px;height:55px;border-radius:17px;display:flex;align-items:center;justify-content:center;font-size:26px;background:linear-gradient(135deg,rgba(34,211,238,.12),rgba(139,92,246,.16));border:1px solid rgba(125,211,252,.15)}
.card h3{font-size:18px;margin:16px 0 7px}.card p{color:#94a3b8;font-size:13px;line-height:1.55;margin:0}
.stat{padding:20px;border-radius:19px;background:rgba(15,23,42,.72);border:1px solid var(--line);animation:pageIn .5s ease both}.stat small{color:#64748b}.stat strong{display:block;font-size:30px;margin-top:5px}
.panel{padding:28px;border-radius:25px;background:rgba(15,23,42,.70);border:1px solid var(--line);animation:pageIn .5s ease}
.status{display:inline-block;padding:6px 10px;border-radius:99px;background:rgba(34,197,94,.10);color:#86efac;font-size:11px;font-weight:700}
.status.closed{background:rgba(148,163,184,.10);color:#cbd5e1}.status.progress{background:rgba(250,204,21,.10);color:#fde68a}
.chat{padding:14px 16px;border-radius:16px;background:rgba(30,41,59,.65);margin:9px 0;animation:pageIn .35s ease}.chat.user{border-left:3px solid #38bdf8}.chat.ai{border-left:3px solid #a78bfa}
.stTextInput input,.stTextArea textarea,.stSelectbox>div>div{background:rgba(15,23,42,.82)!important;color:#f8fafc!important;border:1px solid rgba(148,163,184,.16)!important;border-radius:13px!important}
.stTextInput input:focus,.stTextArea textarea:focus{border-color:rgba(56,189,248,.5)!important;box-shadow:0 0 0 3px rgba(56,189,248,.07)!important}
div[data-testid="stForm"]{background:transparent;border:none}
.footer{text-align:center;color:#64748b;font-size:11px;padding:35px 0 5px}
@keyframes pageIn{from{opacity:0;transform:translateY(20px) scale(.985)}to{opacity:1;transform:none}}
@keyframes float{0%,100%{transform:translateY(0) rotateY(0)}50%{transform:translateY(-18px) rotateY(180deg)}}
@keyframes orbit{to{transform:rotateX(70deg) rotateZ(360deg)}}@keyframes orbit2{to{transform:rotateY(70deg) rotateZ(-360deg)}}
@keyframes glow{0%,100%{transform:scale(1);opacity:.65}50%{transform:scale(1.14);opacity:1}}
@media(max-width:900px){.hero{padding:30px;min-height:480px}.hero h1{font-size:42px}.orb{right:45px;top:285px;width:110px;height:110px}}
/* -------- AI EXPERIENCE -------- */
.ai-shell{position:relative;overflow:hidden;border:1px solid rgba(103,232,249,.14);border-radius:30px;padding:30px;background:radial-gradient(circle at 18% 10%,rgba(34,211,238,.10),transparent 30%),radial-gradient(circle at 90% 20%,rgba(139,92,246,.14),transparent 32%),linear-gradient(145deg,rgba(10,18,36,.96),rgba(8,13,28,.92));box-shadow:0 30px 90px rgba(0,0,0,.32),inset 0 1px rgba(255,255,255,.04);animation:pageIn .6s ease}
.ai-shell:before{content:"";position:absolute;inset:-40%;background:conic-gradient(from 90deg,transparent,rgba(34,211,238,.05),transparent,rgba(139,92,246,.06),transparent);animation:spinBg 16s linear infinite;pointer-events:none}
.ai-grid{position:relative;z-index:2;display:grid;grid-template-columns:310px 1fr;gap:28px}
.ai-core{min-height:480px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;border-radius:25px;background:rgba(15,23,42,.58);border:1px solid rgba(148,163,184,.12);position:relative;overflow:hidden}
.ai-core:after{content:"";position:absolute;width:230px;height:230px;border-radius:50%;background:rgba(34,211,238,.07);filter:blur(40px);animation:pulseGlow 3s ease-in-out infinite}
.ai-orb{width:145px;height:145px;border-radius:50%;position:relative;z-index:3;background:radial-gradient(circle at 30% 22%,#fff 0 4%,#a5f3fc 7%,#22d3ee 18%,#3b82f6 42%,#7c3aed 70%,#111827 100%);box-shadow:0 0 30px rgba(34,211,238,.7),0 0 85px rgba(124,58,237,.38),inset -18px -20px 35px rgba(0,0,0,.25);animation:aiFloat 4s ease-in-out infinite}
.ai-orb:before,.ai-orb:after{content:"";position:absolute;inset:-20px;border:1px solid rgba(103,232,249,.3);border-radius:50%;transform:rotateX(70deg);animation:aiRing 5s linear infinite}
.ai-orb:after{inset:-35px;border-color:rgba(167,139,250,.25);transform:rotateY(70deg);animation:aiRing2 7s linear infinite}
.ai-core h2{position:relative;z-index:4;margin:35px 0 7px;font-size:25px}.ai-core p{position:relative;z-index:4;color:#94a3b8;font-size:12px;max-width:220px;line-height:1.6}
.ai-live{position:relative;z-index:4;margin-top:18px;padding:7px 12px;border-radius:99px;font-size:10px;font-weight:800;letter-spacing:1px;color:#86efac;background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.18)}
.ai-live:before{content:"";display:inline-block;width:7px;height:7px;border-radius:50%;background:#4ade80;margin-right:7px;box-shadow:0 0 12px #4ade80;animation:livePulse 1.5s infinite}
.ai-chat{height:480px;display:flex;flex-direction:column;border-radius:25px;background:rgba(2,6,23,.48);border:1px solid rgba(148,163,184,.11);overflow:hidden}
.ai-chat-head{padding:17px 20px;border-bottom:1px solid rgba(148,163,184,.1);display:flex;align-items:center;gap:12px;background:rgba(15,23,42,.5)}
.ai-mini-avatar{width:36px;height:36px;border-radius:12px;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#22d3ee,#7c3aed);box-shadow:0 0 22px rgba(34,211,238,.22)}
.ai-chat-head strong{font-size:14px}.ai-chat-head small{display:block;color:#64748b;margin-top:2px}
.ai-history{flex:1;overflow:auto;padding:18px}
.ai-msg{max-width:82%;padding:12px 15px;border-radius:17px;margin:9px 0;line-height:1.55;font-size:13px;animation:msgIn .35s ease;white-space:pre-wrap}
.ai-msg.user{margin-left:auto;background:linear-gradient(135deg,rgba(37,99,235,.78),rgba(124,58,237,.72));border-bottom-right-radius:5px;box-shadow:0 10px 28px rgba(37,99,235,.13)}
.ai-msg.bot{background:rgba(30,41,59,.72);border:1px solid rgba(148,163,184,.1);border-bottom-left-radius:5px}
.ai-spark{font-size:10px;color:#67e8f9;font-weight:800;letter-spacing:1px;margin-bottom:5px}
.ai-quick-label{font-size:11px;color:#64748b;margin-top:18px}
.ai-empty{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#64748b}.ai-empty .big{font-size:38px;margin-bottom:10px}.ai-empty strong{color:#cbd5e1;font-size:15px}.ai-empty p{font-size:12px;max-width:360px;line-height:1.6}
.ai-metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px}.ai-metric{padding:12px;border-radius:15px;background:rgba(15,23,42,.65);border:1px solid rgba(148,163,184,.1)}.ai-metric small{color:#64748b}.ai-metric strong{display:block;margin-top:4px;font-size:17px}
@keyframes aiFloat{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-14px) scale(1.035)}}
@keyframes aiRing{to{transform:rotateX(70deg) rotateZ(360deg)}}@keyframes aiRing2{to{transform:rotateY(70deg) rotateZ(-360deg)}}
@keyframes pulseGlow{0%,100%{transform:scale(.9);opacity:.45}50%{transform:scale(1.2);opacity:1}}
@keyframes livePulse{50%{opacity:.35;transform:scale(.7)}}@keyframes msgIn{from{opacity:0;transform:translateY(9px)}to{opacity:1;transform:none}}
@keyframes spinBg{to{transform:rotate(360deg)}}
@media(max-width:900px){.ai-grid{grid-template-columns:1fr}.ai-core{min-height:300px}.ai-chat{height:520px}}

</style>
""", unsafe_allow_html=True)

# ---------------- HELPERS ----------------
def go(page):
    st.session_state.page = page
    st.rerun()

def nav_button(label, page):
    if st.button(label, use_container_width=True, key=f"nav_{page}"):
        go(page)

def page_header(title, subtitle):
    st.markdown(f"""
    <div style="animation:pageIn .5s ease">
      <div class="badge">✦ CAMPUS COPILOT</div>
      <h1 style="font-size:42px;margin:15px 0 5px;letter-spacing:-1.5px">{title}</h1>
      <p class="muted" style="margin-top:0">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def new_ticket():
    return "CC-" + uuid.uuid4().hex[:7].upper()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("""
    <div class="brand">
      <div class="brand-title">🎓 Campus Copilot</div>
      <div class="brand-sub">AI-powered campus assistant</div>
    </div>
    <div class="nav-title">NAVIGATION</div>
    """, unsafe_allow_html=True)

    nav_button("🏠  Home", "Home")
    nav_button("🤖  Ask Campus AI", "AI Assistant")
    nav_button("🛠️  Report a Problem", "Report Problem")
    nav_button("🔎  Lost & Found", "Lost & Found")
    nav_button("📢  Notices & Events", "Notices")
    nav_button("📊  Admin Dashboard", "Admin")

    st.markdown("<br><hr style='border-color:rgba(148,163,184,.12)'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="panel" style="padding:17px">
      <div style="font-weight:700">⚡ Smart Campus</div>
      <div class="muted" style="font-size:12px;margin-top:6px">One place for student support, campus services and issue reporting.</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- HOME ----------------
if st.session_state.page == "Home":
    st.markdown("""
    <div class="hero">
      <div class="hero-content">
        <div class="badge">✦ AI POWERED CAMPUS PLATFORM</div>
        <h1>Campus Copilot</h1>
        <p>Your intelligent campus companion. Find information, report problems, discover services and stay connected with campus activity — from one beautiful workspace.</p>
      </div>
      <div class="orb"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">⚡ Everything students need</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    cards = [
        ("🤖","Ask Campus AI","Get quick answers about departments, facilities, schedules and campus services.","AI Assistant"),
        ("🛠️","Report a Problem","Submit classroom, Wi‑Fi, electricity or infrastructure issues.","Report Problem"),
        ("🔎","Lost & Found","Post a lost item or check items reported by other students.","Lost & Found"),
    ]
    for col,(ic,title,desc,target) in zip(cols,cards):
        with col:
            st.markdown(f'<div class="card"><div class="icon">{ic}</div><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
            if st.button(f"Open {title} →", key=f"home_{target}", use_container_width=True):
                go(target)

    st.markdown('<div class="section-title">📊 Campus at a glance</div>', unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    stats=[("Active Services","12"),("Issues Reported",str(len(st.session_state.complaints))),("Lost Items",str(len(st.session_state.lost_found))),("AI Queries",str(len(st.session_state.messages)//2))]
    for col,(label,num) in zip([c1,c2,c3,c4],stats):
        with col: st.markdown(f'<div class="stat"><small>{label}</small><strong>{num}</strong></div>',unsafe_allow_html=True)

    st.markdown('<div class="section-title">🚀 Quick actions</div>', unsafe_allow_html=True)
    q1,q2,q3=st.columns(3)
    with q1:
        if st.button("📢 View latest notices", use_container_width=True): go("Notices")
    with q2:
        if st.button("📊 Open admin dashboard", use_container_width=True): go("Admin")
    with q3:
        if st.button("💬 Start with Campus AI", use_container_width=True): go("AI Assistant")

# ---------------- AI ----------------
def campus_ai_answer(prompt):
    q = prompt.lower()
    if "cse" in q or "computer" in q:
        return "The CSE department can be listed in the academic block directory. In a production version, I can connect to your official campus map and department database."
    if "library" in q:
        return "The library module can show timings, floor information, facilities and available resources."
    if "hostel" in q:
        return "The hostel module can show blocks, wardens, timings, mess details and maintenance reporting."
    if "complaint" in q or "problem" in q:
        return "Use Report a Problem to submit an issue. You will receive a ticket ID, and the admin can update its status."
    if "lost" in q or "found" in q:
        return "Open Lost & Found to add a Lost/Found listing and browse recent campus listings."
    if "notice" in q or "event" in q:
        return "Open Notices & Events to browse campus updates. You can also filter notices by category."
    if "placement" in q or "job" in q:
        return "For placements, Campus Copilot can provide workshop notices, preparation resources and placement-cell updates when connected to the official campus data."
    return "I can help with campus services, departments, facilities, complaints, placements, Lost & Found and notices. Try one of the quick prompts below."

def ask_ai(prompt):
    prompt = prompt.strip()
    if not prompt:
        return
    st.session_state.messages.append(("user", prompt))
    st.session_state.messages.append(("ai", campus_ai_answer(prompt)))
    st.rerun()

if st.session_state.page == "AI Assistant":
    page_header("Campus AI", "Your intelligent campus companion — ask, explore and get instant guidance.")

    st.markdown('<div class="ai-shell"><div class="ai-grid">', unsafe_allow_html=True)

    st.markdown('''
    <div class="ai-core">
      <div class="ai-orb"></div>
      <h2>Campus Intelligence</h2>
      <p>Powered by your campus knowledge base. Ask naturally — no complicated commands.</p>
      <div class="ai-live">LIVE AI CORE</div>
      <div class="ai-metrics" style="width:90%">
        <div class="ai-metric"><small>Queries</small><strong>''' + str(len(st.session_state.messages)//2) + '''</strong></div>
        <div class="ai-metric"><small>Mode</small><strong>Smart</strong></div>
        <div class="ai-metric"><small>Status</small><strong>Online</strong></div>
      </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('<div class="ai-chat"><div class="ai-chat-head"><div class="ai-mini-avatar">✦</div><div><strong>Campus Copilot AI</strong><small>Ready to help with campus questions</small></div></div><div class="ai-history">', unsafe_allow_html=True)
    if not st.session_state.messages:
        st.markdown('<div class="ai-empty"><div class="big">✦</div><strong>How can I help you today?</strong><p>Ask about departments, library, hostel, complaints, placements, events or Lost & Found.</p></div>', unsafe_allow_html=True)
    else:
        for role, msg in st.session_state.messages[-10:]:
            if role == "user":
                st.markdown(f'<div class="ai-msg user">{msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ai-msg bot"><div class="ai-spark">✦ CAMPUS AI</div>{msg}</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="ai-quick-label">QUICK PROMPTS</div>', unsafe_allow_html=True)
    q1,q2,q3,q4=st.columns(4)
    with q1:
        if st.button("📚 Library",key="quick_library",use_container_width=True): ask_ai("Where is the library and what information can I get?")
    with q2:
        if st.button("💻 CSE Department",key="quick_cse",use_container_width=True): ask_ai("Tell me about the CSE department")
    with q3:
        if st.button("🎯 Placements",key="quick_placement",use_container_width=True): ask_ai("Tell me about placements")
    with q4:
        if st.button("🛠️ Report issue",key="quick_issue",use_container_width=True): ask_ai("How can I report a campus problem?")

    user_prompt=st.chat_input("Ask Campus Copilot anything about your campus...")
    if user_prompt:
        ask_ai(user_prompt)

    if st.button("🧹 Clear conversation",key="clear_ai_chat",use_container_width=True):
        st.session_state.messages=[]
        st.rerun()

# ---------------- REPORT ----------------
elif st.session_state.page == "Report Problem":
    page_header("Report a Problem", "Submit an issue and receive a trackable ticket ID.")
    with st.form("problem_form", clear_on_submit=True):
        c1,c2=st.columns(2)
        with c1:
            category=st.selectbox("Category",["Classroom","Wi‑Fi / Network","Electricity","Lab","Hostel","Cleanliness","Other"])
            location=st.text_input("Location",placeholder="Example: CSE Block, Room 204")
        with c2:
            priority=st.selectbox("Priority",["Normal","High","Urgent"])
            title=st.text_input("Short title",placeholder="Example: Wi‑Fi not working")
        description=st.text_area("Describe the problem",placeholder="Add useful details...")
        submit=st.form_submit_button("🚀 Submit Report",use_container_width=True)

    if submit:
        if title.strip() and description.strip():
            ticket=new_ticket()
            st.session_state.complaints.append({
                "ticket":ticket,"title":title.strip(),"category":category,"location":location.strip(),
                "priority":priority,"description":description.strip(),
                "time":datetime.now().strftime("%d %b %Y, %I:%M %p"),"status":"Open"
            })
            st.success(f"Report submitted successfully! Ticket ID: {ticket}")
            st.balloons()
        else:
            st.warning("Please add a title and description.")

    if st.session_state.complaints:
        st.markdown('<div class="section-title">Recent reports</div>',unsafe_allow_html=True)
        for item in reversed(st.session_state.complaints[-5:]):
            st.markdown(f'<div class="card" style="min-height:auto;margin-bottom:12px"><span class="status">{item["status"]}</span><h3>{item["title"]}</h3><p><b>{item["ticket"]}</b> · {item["category"]} · {item["location"] or "Location not specified"} · {item["time"]}</p></div>',unsafe_allow_html=True)

# ---------------- LOST & FOUND ----------------
elif st.session_state.page == "Lost & Found":
    page_header("Lost & Found", "Add a listing or browse items reported by students.")
    with st.form("lost_form", clear_on_submit=True):
        c1,c2=st.columns(2)
        with c1: item=st.text_input("Item",placeholder="Example: Black wallet")
        with c2: kind=st.selectbox("Type",["Lost","Found"])
        place=st.text_input("Where?",placeholder="Example: Library")
        details=st.text_area("Details",placeholder="Add identifying information without sensitive personal data.")
        submit=st.form_submit_button("➕ Add Listing",use_container_width=True)
    if submit:
        if item.strip():
            st.session_state.lost_found.append({
                "item":item.strip(),"kind":kind,"place":place.strip(),"details":details.strip(),
                "time":datetime.now().strftime("%d %b %Y, %I:%M %p")
            })
            st.success("Listing added successfully.")
        else:
            st.warning("Please enter an item name.")

    if st.session_state.lost_found:
        st.markdown('<div class="section-title">Recent listings</div>',unsafe_allow_html=True)
        cols=st.columns(3)
        for i,x in enumerate(reversed(st.session_state.lost_found[-9:])):
            with cols[i%3]:
                st.markdown(f'<div class="card" style="margin-bottom:15px"><div class="icon">{"🔴" if x["kind"]=="Lost" else "🟢"}</div><h3>{x["item"]}</h3><p><b>{x["kind"]}</b> · {x["place"] or "Place not specified"}</p><p style="margin-top:8px">{x["details"] or "No extra details."}</p><p style="margin-top:10px;font-size:11px">{x["time"]}</p></div>',unsafe_allow_html=True)
    else:
        st.info("No listings yet. Add the first one above.")

# ---------------- NOTICES ----------------
elif st.session_state.page == "Notices":
    page_header("Notices & Events", "Important campus updates in one clean feed.")
    filter_value=st.selectbox("Filter",["All","Academic","Career","Events","Library"])
    notices=[
        ("📢","Hackathon registration","Events","Student innovation registrations are now open."),
        ("🎓","Placement workshop","Career","A career preparation session can be listed here with venue and timing."),
        ("🏆","Campus innovation challenge","Events","Showcase your prototype and solve a real campus problem."),
        ("📚","Library update","Library","Library timings and resource availability can be published here."),
        ("📝","Academic schedule update","Academic","Important academic schedule information can be published here."),
    ]
    visible=[n for n in notices if filter_value=="All" or n[2]==filter_value]
    for ic,title,category,desc in visible:
        st.markdown(f'<div class="card" style="min-height:auto;margin-bottom:13px;display:flex;gap:18px;align-items:center"><div class="icon">{ic}</div><div><span class="status">{category}</span><h3 style="margin:9px 0 6px">{title}</h3><p>{desc}</p></div></div>',unsafe_allow_html=True)
    if st.button("🔄 Reset notice filter",use_container_width=True):
        st.rerun()

# ---------------- ADMIN ----------------
elif st.session_state.page == "Admin":
    page_header("Admin Dashboard", "Monitor reports and change issue status from one place.")
    c1,c2,c3,c4=st.columns(4)
    stats=[("Total Reports",len(st.session_state.complaints)),("Open",sum(x["status"]=="Open" for x in st.session_state.complaints)),("In Progress",sum(x["status"]=="In Progress" for x in st.session_state.complaints)),("Closed",sum(x["status"]=="Closed" for x in st.session_state.complaints))]
    for col,(label,num) in zip([c1,c2,c3,c4],stats):
        with col: st.markdown(f'<div class="stat"><small>{label}</small><strong>{num}</strong></div>',unsafe_allow_html=True)

    st.markdown('<div class="section-title">🛠️ Issue Queue</div>',unsafe_allow_html=True)
    if not st.session_state.complaints:
        st.info("No reports yet. Submit one from Report a Problem.")
    else:
        for i,item in enumerate(reversed(st.session_state.complaints)):
            idx=len(st.session_state.complaints)-1-i
            st.markdown(f'<div class="card" style="min-height:auto;margin-bottom:12px"><span class="status {"closed" if item["status"]=="Closed" else "progress" if item["status"]=="In Progress" else ""}">{item["status"]}</span><h3>{item["title"]}</h3><p><b>{item["ticket"]}</b> · {item["category"]} · {item["priority"]} · {item["location"] or "No location"}</p><p style="margin-top:8px">{item["description"]}</p></div>',unsafe_allow_html=True)
            b1,b2,b3=st.columns(3)
            with b1:
                if st.button("🟡 In Progress",key=f"progress_{item['ticket']}",use_container_width=True):
                    st.session_state.complaints[idx]["status"]="In Progress"; st.rerun()
            with b2:
                if st.button("🟢 Close",key=f"close_{item['ticket']}",use_container_width=True):
                    st.session_state.complaints[idx]["status"]="Closed"; st.rerun()
            with b3:
                if st.button("🔵 Reopen",key=f"reopen_{item['ticket']}",use_container_width=True):
                    st.session_state.complaints[idx]["status"]="Open"; st.rerun()

st.markdown('<div class="footer">Campus Copilot · Built for smarter campus experiences · Hackathon Prototype</div>',unsafe_allow_html=True)
