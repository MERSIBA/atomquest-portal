import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
DB_FILE = 'atomquest_portal.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, role TEXT, manager_id INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS goal_sheets (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, status TEXT DEFAULT "Draft")')
    cursor.execute('CREATE TABLE IF NOT EXISTS goals (id INTEGER PRIMARY KEY AUTOINCREMENT, sheet_id INTEGER, thrust_area TEXT, title TEXT, description TEXT, uom_type TEXT, target_val REAL, weightage REAL, actual_achievement REAL DEFAULT 0, status TEXT DEFAULT "Not Started")')
    for uid, name, r, mid in [(1, 'employee_test', 'Employee', 2), (2, 'manager_test', 'Manager', 3), (3, 'admin_test', 'Admin', None)]:
        try: cursor.execute('INSERT INTO users VALUES (?,?,?,?)', (uid, name, r, mid))
        except sqlite3.IntegrityError: pass
    conn.commit()
    conn.close()

def check_business_rules(goals):
    if len(goals) > 8: return False, "Limit Exceeded: Max 8 goals allowed per sheet."
    if any(float(g.get('weightage', 0)) < 10 for g in goals): return False, "Floor Error: Min weightage per goal is 10%."
    if sum(float(g.get('weightage', 0)) for g in goals) != 100: return False, "Balance Error: Total sheet weight must sum to exactly 100%."
    return True, "Valid"

@app.route('/api/employee/submit', methods=['POST'])
def submit_sheet():
    data = request.json or {}
    goals = data.get('goals', [])
    ok, err = check_business_rules(goals)
    if not ok: return jsonify({"status": "Failed", "message": err}), 400
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO goal_sheets (user_id, status) VALUES (?, "Pending Approval")', (data.get('user_id', 1),))
    sid = cursor.lastrowid
    for g in goals:
        cursor.execute('INSERT INTO goals (sheet_id, thrust_area, title, description, uom_type, target_val, weightage) VALUES (?,?,?,?,?,?,?)', (sid, g['thrust_area'], g['title'], g['description'], g['uom_type'], g['target_val'], g['weightage']))
    conn.commit()
    conn.close()
    return jsonify({"status": "Success", "message": "Goal sheet successfully validated and locked into manager review pool."})

@app.route('/')
def interface():
    return render_template_string('''<!DOCTYPE html>
<html>
<head>
    <title>Atomberg Goal System Portal</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-900 p-8 flex items-center justify-center min-h-screen font-sans">
    <div class="max-w-xl w-full bg-gray-800 p-6 rounded-xl shadow-2xl border border-gray-700">
        <div class="border-b border-gray-700 pb-4 mb-5">
            <h1 class="text-xl font-bold text-white tracking-wide">AtomQuest 1.0 Evaluation Engine</h1>
            <p class="text-xs text-yellow-500 font-medium tracking-wider uppercase mt-1">In-House Goal Setting & Tracking Portal</p>
            <div class="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-gray-700/50 text-[11px] text-gray-400">
                <div><span class="text-gray-500">Track:</span> Data Engineering & Backend</div>
                <div><span class="text-gray-500">Benchmark:</span> Adherence & Architecture Optimization</div>
            </div>
        </div>

        <button onclick="runTest()" class="w-full bg-yellow-500 hover:bg-yellow-600 text-gray-950 font-bold text-xs uppercase py-3 px-4 rounded shadow-md transition-all duration-150 transform active:scale-[0.99]">
            Run Phase 1 Boundary Interceptor Check
        </button>

        <div class="mt-5">
            <div class="flex items-center justify-between mb-1">
                <span class="text-[11px] font-bold uppercase tracking-wider text-gray-400">System Transaction Logs:</span>
                <span class="inline-flex items-center px-1.5 py-0.5 rounded-full text-[10px] font-medium bg-green-900/50 text-green-400 border border-green-800">
                    ● Engine Online
                </span>
            </div>
            <div id="out" class="p-3.5 bg-black/80 text-green-400 font-mono text-xs rounded-lg h-28 border border-gray-900 overflow-y-auto shadow-inner leading-relaxed">>> Initialization parameters verified. Local server listening on pipeline port 8080...</div>
        </div>
    </div>

    <script>
    function runTest(){
        fetch('/api/employee/submit',{
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({
                user_id:1,
                goals:[
                    {thrust_area:'R&D',title:'BLDC Tuning',description:'Optimization',uom_type:'Min',target_val:95,weightage:60},
                    {thrust_area:'Ops',title:'Noise Dampening',description:'Testing',uom_type:'Max',target_val:2,weightage:40}
                ]
            })
        })
        .then(function(r){ return r.json(); })
        .then(function(d){
            document.getElementById('out').innerText += '\\n>> Routing validation structure to interceptor pipeline...\\n>> Response: ' + d.message;
            var obj = document.getElementById('out');
            obj.scrollTop = obj.scrollHeight;
        })
        .catch(function(err){
            document.getElementById('out').innerText += '\\n>> Connection Error to local network adapter.';
        });
    }
    </script>
</body>
</html>''')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8080)
