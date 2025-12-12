import { useState, useEffect } from 'react'
import { getTasks, updateTask, getUsers, createUser, createTask } from './api'
import './App.css'

function App() {
    const [tasks, setTasks] = useState([])
    const [users, setUsers] = useState([])
    const [selectedUser, setSelectedUser] = useState(null)
    const [newTaskTitle, setNewTaskTitle] = useState('')

    useEffect(() => {
        fetchData()
    }, [])

    const fetchData = async () => {
        const t = await getTasks()
        setTasks(t)
        const u = await getUsers()
        setUsers(u)
        if (u.length > 0 && !selectedUser) {
            setSelectedUser(u[0].id)
        }
    }

    const handleToggleComplete = async (task) => {
        // BUG: This is where the frontend sends the update.
        // The backend has a bug where it ignores 'is_completed' if it's false? 
        // Or maybe we send it wrong?
        // Let's send the whole object with the flipped boolean.
        try {
            await updateTask(task.id, {
                ...task,
                is_completed: !task.is_completed
            })
            fetchData()
        } catch (error) {
            console.error("Failed to update task", error)
        }
    }

    const handleCreateTask = async (e) => {
        e.preventDefault()
        if (!selectedUser) return;
        try {
            await createTask(selectedUser, {
                title: newTaskTitle,
                description: "Created via frontend",
                is_completed: false
            })
            setNewTaskTitle('')
            fetchData()
        } catch (error) {
            console.error("Failed to create task", error)
        }
    }

    return (
        <div className="container">
            <h1>Team Task Manager</h1>

            <div className="controls">
                <select onChange={(e) => setSelectedUser(e.target.value)} value={selectedUser || ''}>
                    {users.map(u => <option key={u.id} value={u.id}>{u.email}</option>)}
                </select>
                <form onSubmit={handleCreateTask} style={{ display: 'inline-block', marginLeft: '10px' }}>
                    <input
                        type="text"
                        value={newTaskTitle}
                        onChange={(e) => setNewTaskTitle(e.target.value)}
                        placeholder="New Task Title"
                    />
                    <button type="submit">Add Task</button>
                </form>
            </div>

            <div className="task-list">
                {tasks.map(task => (
                    <div key={task.id} className={`task-item ${task.is_completed ? 'completed' : ''}`}>
                        <input
                            type="checkbox"
                            checked={task.is_completed}
                            onChange={() => handleToggleComplete(task)}
                        />
                        <span className="task-title">{task.title}</span>
                        <span className="task-owner">Owner: {task.owner_id}</span>
                        {/* Task 1: Candidate needs to add Priority display here */}
                    </div>
                ))}
            </div>
        </div>
    )
}

export default App
