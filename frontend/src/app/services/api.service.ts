import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface User {
    id?: number;
    email: string;
    is_active: boolean;
    tasks?: Task[];
}

export interface Task {
    id?: number;
    title: string;
    description?: string;
    is_completed: boolean;
    owner_id?: number;
    owner?: number;
}

@Injectable({
    providedIn: 'root'
})
export class ApiService {
    private baseUrl = 'http://127.0.0.1:8000'; // Django default port

    constructor(private http: HttpClient) { }

    getUsers(): Observable<User[]> {
        return this.http.get<User[]>(`${this.baseUrl}/users/`);
    }

    createUser(user: User): Observable<User> {
        return this.http.post<User>(`${this.baseUrl}/users/`, user);
    }

    getTasks(): Observable<Task[]> {
        return this.http.get<Task[]>(`${this.baseUrl}/tasks/`);
    }

    createTask(task: Task): Observable<Task> {
        return this.http.post<Task>(`${this.baseUrl}/tasks/`, task);
    }

    updateTask(taskId: number, task: Task): Observable<Task> {
        return this.http.put<Task>(`${this.baseUrl}/tasks/${taskId}/`, task);
    }
}
