import { Component, OnInit, ChangeDetectorRef } from '@angular/core';

import { HttpClientModule } from '@angular/common/http';

import { IpInfo } from './ip-get.model';
import { IpGetServiceService } from "./ip-get-service.service";
import * as publicIp  from 'public-ip';


@Component({
  selector: 'app-ipget',
  standalone: true,
  imports: [HttpClientModule],
  templateUrl: './ipget.component.html',
  styleUrl: './ipget.component.css'
})
export class IpGetSComponent implements OnInit {
  ipInfo: IpInfo = { ip: { ip: '', country_short: '', country_long: '', region: '', city: '' } };

  constructor(private ipService: IpGetServiceService, private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
      publicIp.publicIpv4().then((ip)=>{
          this.ipService.getIpInfo(ip).subscribe(
              (data: IpInfo) => {
                  this.ipInfo = data;
                  console.log(data)
                  this.cdr.markForCheck(); // Forzar la detección de cambios
              },
              (error) => {
                  console.error('Error fetching IP info:', error);
              }
          );
      })
  }
}