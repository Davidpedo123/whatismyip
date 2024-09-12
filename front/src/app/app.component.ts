import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { IpService } from './ip.service';
import { IpInfo } from './ip.model';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
    ipInfo: IpInfo = { ip: { ip: '', country_short: '', country_long: '', region: '', city: '' } };

    constructor(private ipService: IpService, private cdr: ChangeDetectorRef) {}

    ngOnInit(): void {
        const ipToFetch = '8.8.8.8';

        this.ipService.getIpInfo(ipToFetch).subscribe(
            (data: IpInfo) => {
                this.ipInfo = data;
                console.log(data)
                this.cdr.markForCheck(); // Forzar la detección de cambios
            },
            (error) => {
                console.error('Error fetching IP info:', error);
            }
        );
    }
}
