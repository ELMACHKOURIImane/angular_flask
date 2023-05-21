import { Component } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { CarServiceService } from '../car-service.service';
import { CarModule } from '../car/car.module';

@Component({
  selector: 'app-update',
  templateUrl: './update.component.html',
  styleUrls: ['./update.component.css']
})
export class UpdateComponent{

  car = new  CarModule();
  id_car!: number;
  model!: string;
  hp!: number;
  marque!: string;
  carToUpdate!:CarModule;
  constructor(private router:Router , private carServices:CarServiceService , private activatedRoute:ActivatedRoute){
    this.activatedRoute.params.subscribe(param =>{
      this.id_car = param['id'];
       this.carServices.getOneCar(this.id_car).subscribe(response=>{
        console.log(response)
        this.hp = response.hp
        this.model = response.model
        this.marque = response.marque
       })
    })


  }
  update(){
    this.car.id_car = this.id_car;
    this.car.model = this.model;
    this.car.hp = this.hp;
    this.car.marque = this.marque;
    this.carServices.updateCar(this.car).subscribe();
  }



}
