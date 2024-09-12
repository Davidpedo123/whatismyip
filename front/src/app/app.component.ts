import { Component, OnInit } from '@angular/core';
import { IpService } from './ip.service';
import { IpInfo } from './ip.model';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
    ipInfo: IpInfo | null = null;

    constructor(private ipService: IpService) {}

    ngOnInit(): void {
        const ipToFetch = '8.8.8.8';
        this.ipService.getIpInfo(ipToFetch).subscribe(
            (data: IpInfo) => {
                this.ipInfo = data;
            },
            (error) => {
                console.error('Error fetching IP info:', error);
            }
        );
    }
}
