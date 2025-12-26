import { Component, OnInit } from '@angular/core';
import { ApiService, User } from '../../services/api.service';

@Component({
    selector: 'app-user-list',
    templateUrl: './user-list.component.html',
    styleUrls: ['./user-list.component.css']
})
export class UserListComponent implements OnInit {
    users: User[] = [];
    newUser: User = { email: '', is_active: true };

    constructor(private apiService: ApiService) { }

    ngOnInit(): void {
        this.loadUsers();
    }

    loadUsers() {
        this.apiService.getUsers().subscribe(users => {
            this.users = users;
        });
    }

    createUser() {
        if (!this.newUser.email) return;
        this.apiService.createUser(this.newUser).subscribe(user => {
            this.users.push(user);
            this.newUser = { email: '', is_active: true };
        });
    }
}
