import { Component, OnInit } from '@angular/core';
import { UserModelModule } from '../user-model/user-model.module';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { CarServiceService } from '../car-service.service';
import { Token } from '@angular/compiler';
import { HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit{
  username = '';
  password = '';

  constructor(private router: Router, private carService: CarServiceService) {
    localStorage.setItem('token', '');
  }
  ngOnInit(): void {
  }

  Login(){
    let myHeaders = new Headers();
    myHeaders.append('Content-Type', 'application/json');


    let raw = JSON.stringify({
      username: this.username,
      password: this.password,
    });
    let requestOptions: RequestInit = {
      method: 'POST',
      headers: myHeaders ,
      body: raw,
      redirect: 'follow',

    };
    fetch('http://localhost:5000/login', requestOptions)
      .then((response) => response.json())
      .then((result) =>{
        localStorage.setItem('token', result.data.token);
        console.log(result.data.jwt);
        window.location.href = '/lisofcars';
      })
      .catch((error) => console.log('error', error));
  }
}
