import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { CarModule } from './car/car.module';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CarServiceService {

  // url principal
  url:string = "http://127.0.0.1:5000";
  token = localStorage.getItem('token');

   httpOptions = {
    headers: new HttpHeaders(
    {
       'Authorization': `Bearer ${this.token}`,
       'Content-Type': 'application/json'
    })
}

  constructor(private http:HttpClient) { }


  saveCare(car:CarModule){

    console.log(this.url+"/savecar");

    console.log("car service" + car);
    return this.http.post(this.url+"/savecar" , car , this.httpOptions );

  }
  getAllcars():Observable<CarModule[]>{

     return  this.http.get<CarModule[]>(this.url+"/cars" ,this.httpOptions);
  }
  getOneCar(car_id:number):Observable<CarModule>{
    return this.http.get<CarModule>(this.url+`/car/${car_id}`)
  }
  dleteCarById(carId:number){
    return this.http.get(this.url + `/delete/${carId}` , this.httpOptions);
  }
  updateCar(car:CarModule){
    return this.http.post(this.url+`/update/${car.id_car}`, car ,this.httpOptions);
  }



}
