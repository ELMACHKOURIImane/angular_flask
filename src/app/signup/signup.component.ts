import { Component } from '@angular/core';
import { UserModelModule } from '../user-model/user-model.module';
import { Router } from '@angular/router';
import { CarServiceService } from '../car-service.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {
  username = '';
  password = '';

  constructor(private router: Router, private carService: CarServiceService) {
    localStorage.setItem('token', '');
  }

  saveUser(){
    let myHeaders = new Headers();
    myHeaders.append('Content-Type', 'application/json');

    let raw = JSON.stringify({
      username: this.username,
      password: this.password,
    });

    let requestOptions: RequestInit = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow',
    };

    fetch('http://localhost:5000/adduser', requestOptions)
      .then((response) => response.json())
      .then((result) => {
        localStorage.setItem('token', result.data.token);
        window.location.href = '/login';
      })
      .catch((error) => console.log('error', error));
  }
}
