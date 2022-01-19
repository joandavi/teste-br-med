import { Component, OnInit } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import { FormGroup, FormBuilder} from '@angular/forms';
import { RatesDates } from './rates-dates';

import * as Highcharts from 'highcharts';
 
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'DesafioBRMed-app';
  dateForm: FormGroup;
  Highcharts: typeof Highcharts = Highcharts;
  chartBrl: any;
  chartEur: any;
  chartJpy: any;
  dates: string[]=[]
  brl: number[]=[]
  eur: number[]=[]
  jpy: number[]=[]
  ApiUrl="http://localhost:8000/api/currencies"				
  constructor(
    private http: HttpClient,
    private df: FormBuilder
  ){}
  ngOnInit(){
    this.getLatestsRates();
    this.createForm(new RatesDates());
  }
  createForm(dateRate: RatesDates) {
    this.dateForm = this.df.group({
      start_date: [dateRate.start_date],
      end_date: [dateRate.end_date],
    })
  }
  getLatestsRates(){
    this.http.get(this.ApiUrl).subscribe((data:any)=>{
      this.fillData(data)
      this.buildCharts()
    }) 
  }
  getRatesByDate(){
    this.http.get(
      this.ApiUrl+`?star_date=${this.dateForm.value.start_date}&end_date=${this.dateForm.value.end_date}`
    ).subscribe((data:any)=>{
      this.resetGraph();
      this.fillData(data)
      this.buildCharts()
    }) 
  }
  fillData(data: any){
    data.forEach((element: {
      date: string; brl: string; jpy: string; eur: string; 
     }) => {
     this.dates.push(element.date)
     this.brl.push(Number(element.brl))
     this.jpy.push(Number(element.jpy))
     this.eur.push(Number(element.eur))
   });
  }
  buildCharts(){
    this.chartBrl = {
      title: {
        text: 'Cotaçoes do Real'
      },
      yAxis: {
        title: {
          text: 'Cotaçao'
        }
      },
      xAxis:{
        categories:this.dates,
    },
      series: [
        {
          type: 'line',
          name:'Real',
          data: this.brl
        }
      ],
      responsive: {
          rules: [{
              condition: {
                  maxWidth: 500
              }
          }]
      },
    };
    this.chartEur = {
      title: {
        text: 'Cotaçoes do Euro'
      },
      yAxis: {
        title: {
          text: 'Cotaçao'
        }
      },
      xAxis:{
        categories:this.dates,
    },
      series: [
        {
          type: 'line',
          name: 'Euro',
          data: this.eur
        }
      ],
      responsive: {
          rules: [{
              condition: {
                  maxWidth: 500
              }
          }]
      },
    };
    this.chartJpy = {
      title: {
        text: 'Cotaçoes do Yene'
      },
      yAxis: {
        title: {
          text: 'Cotaçao'
        }
      },
      xAxis:{
        categories:this.dates,
    },
      series: [
        {
          type: 'line',
          name: 'Yene',
          data: this.jpy
        }
      ],
      responsive: {
          rules: [{
              condition: {
                  maxWidth: 500
              }
          }]
      },
    };
  }
  resetGraph(){
    this.dates = []
    this.brl = []
    this.jpy = []
    this.eur = []
  }
}