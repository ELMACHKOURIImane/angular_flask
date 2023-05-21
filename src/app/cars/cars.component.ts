import { Component } from '@angular/core';
import { NgModel } from '@angular/forms';
import { CarModule } from '../car/car.module';
import { CarServiceService } from '../car-service.service';
import { Route, Router } from '@angular/router';

@Component({
  selector: 'app-cars',
  templateUrl: './cars.component.html',
  styleUrls: ['./cars.component.css']
})
export class CarsComponent {


  cars!:CarModule[];


constructor(private myservice:CarServiceService , private router:Router){
  this.myservice.getAllcars().subscribe(

      (data)=>{

        this.cars = data;
      }


  );
}

deleteCar(id_car:number){
   this.myservice.dleteCarById(id_car).subscribe();
   this.router.navigate(['/lisofcars'])
}


}
