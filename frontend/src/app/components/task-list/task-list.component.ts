import { Component, OnInit } from '@angular/core';
import { ApiService, Task, User } from '../../services/api.service';

@Component({
    selector: 'app-task-list',
    templateUrl: './task-list.component.html',
    styleUrls: ['./task-list.component.css']
})
export class TaskListComponent implements OnInit {
    tasks: Task[] = [];
    users: User[] = [];
    newTask: Task = { title: '', is_completed: false, owner_id: undefined };

    constructor(private apiService: ApiService) { }

    ngOnInit(): void {
        this.loadTasks();
        this.loadUsers();
    }

    loadTasks() {
        this.apiService.getTasks().subscribe(tasks => {
            this.tasks = tasks;
        });
    }

    loadUsers() {
        this.apiService.getUsers().subscribe(users => {
            this.users = users;
            if (users.length > 0 && !this.newTask.owner_id) {
                this.newTask.owner_id = users[0].id;
            }
        });
    }

    createTask() {
        if (!this.newTask.title || !this.newTask.owner_id) return;
        this.apiService.createTask(this.newTask).subscribe(task => {
            this.tasks.push(task);
            this.newTask = { ...this.newTask, title: '' };
        });
    }

    toggleTask(task: Task) {
        if (!task.id) return;
        const updatedTask = { ...task, is_completed: !task.is_completed };
        this.apiService.updateTask(task.id, updatedTask).subscribe(res => {
            task.is_completed = res.is_completed;
        });
    }
}
