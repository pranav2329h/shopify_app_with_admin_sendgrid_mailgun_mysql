import React from 'react'

type Settings = {
  welcome_enabled: boolean
  cart_reminder_enabled: boolean
  cart_reminder_delay_hours: number
  wishlist_reminder_enabled: boolean
  wishlist_reminder_delay_hours: number
}

export default function App(){
  const [shop, setShop] = React.useState('your-store.myshopify.com')
  const [settings, setSettings] = React.useState<Settings | null>(null)
  const [logs, setLogs] = React.useState<any[]>([])
  const [busy, setBusy] = React.useState(false)

  const load = async () => {
    const s = await fetch(`/admin/settings/${shop}`).then(r=>r.json())
    setSettings(s)
    const l = await fetch(`/admin/logs/${shop}`).then(r=>r.json())
    setLogs(l)
  }
  React.useEffect(()=>{ load() }, [])

  const save = async () => {
    if(!settings) return
    setBusy(true)
    await fetch(`/admin/settings/${shop}`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(settings)})
    setBusy(false)
    load()
  }

  return (
    <div style={{fontFamily:'Inter, system-ui, Arial', padding:24}}>
      <h2>Silvee 925 – Auto Email App</h2>
      <div style={{border:'1px solid #e5e7eb', borderRadius:14, padding:16, marginBottom:16}}>
        <label style={{display:'flex', gap:8, alignItems:'center'}}>
          Shop domain:
          <input value={shop} onChange={e=>setShop(e.target.value)} style={{width:280}} />
          <span style={{color:'#6b7280', fontSize:12}}>Permanent domain (e.g., my-store.myshopify.com)</span>
        </label>
        <button onClick={load}>Refresh</button>
      </div>
      {settings && (
        <div style={{display:'grid', gap:16, gridTemplateColumns:'1fr 1fr'}}>
          <div style={{border:'1px solid #e5e7eb', borderRadius:14, padding:16}}>
            <h3>Settings</h3>
            <label><input type="checkbox" checked={settings.welcome_enabled} onChange={e=>setSettings({...settings, welcome_enabled:e.target.checked})}/> Welcome Email</label><br/>
            <label><input type="checkbox" checked={settings.cart_reminder_enabled} onChange={e=>setSettings({...settings, cart_reminder_enabled:e.target.checked})}/> Cart Reminder</label><br/>
            <label>Cart Delay (hrs): <input type="number" value={settings.cart_reminder_delay_hours} onChange={e=>setSettings({...settings, cart_reminder_delay_hours: parseInt(e.target.value||'0')})} style={{width:90}}/></label><br/>
            <label><input type="checkbox" checked={settings.wishlist_reminder_enabled} onChange={e=>setSettings({...settings, wishlist_reminder_enabled:e.target.checked})}/> Wishlist Reminder</label><br/>
            <label>Wishlist Delay (hrs): <input type="number" value={settings.wishlist_reminder_delay_hours} onChange={e=>setSettings({...settings, wishlist_reminder_delay_hours: parseInt(e.target.value||'0')})} style={{width:90}}/></label><br/>
            <button onClick={save} disabled={busy}>{busy?'Saving…':'Save Settings'}</button>
          </div>
          <div style={{border:'1px solid #e5e7eb', borderRadius:14, padding:16}}>
            <h3>Recent Emails</h3>
            <table style={{width:'100%', borderCollapse:'collapse'}}>
              <thead><tr><th style={{textAlign:'left'}}>Recipient</th><th style={{textAlign:'left'}}>Subject</th><th style={{textAlign:'left'}}>Sent At</th></tr></thead>
              <tbody>
                {logs.map((r,i)=> (
                  <tr key={i}><td>{r.recipient}</td><td>{r.subject}</td><td>{new Date(r.sent_at).toLocaleString()}</td></tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}