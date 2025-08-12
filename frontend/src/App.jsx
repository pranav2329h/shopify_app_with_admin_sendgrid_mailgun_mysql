import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const fetchLogs = async () => {
      const response = await axios.get("http://localhost:5000/logs");
      setLogs(response.data);
    };

    fetchLogs();
    const interval = setInterval(fetchLogs, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">📨 Email Logs</h1>
      <div className="grid grid-cols-1 gap-4">
        {logs.map((log) => (
          <div key={log.id} className="border p-4 rounded shadow">
            <div><strong>To:</strong> {log.recipient}</div>
            <div><strong>Subject:</strong> {log.subject}</div>
            <div><strong>Sent At:</strong> {new Date(log.sent_at).toLocaleString()}</div>
            <div><strong>Body:</strong> <div dangerouslySetInnerHTML={{ __html: log.body }} /></div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;