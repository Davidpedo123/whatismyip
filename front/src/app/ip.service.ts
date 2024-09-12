// src/app/ip.service.ts  
import { Injectable } from '@angular/core';  
import { HttpClient } from '@angular/common/http';  
import { Observable } from 'rxjs';  
import { IpInfo } from './ip.model';  

@Injectable({  
    providedIn: 'root'  
})  
export class IpService {  
    private apiUrl = 'http://nginx:80/get-ip'; // Cambia esto por la URL de tu API  

    constructor(private http: HttpClient) {}  

    getIpInfo(ip: string): Observable<IpInfo> {  
        return this.http.get<IpInfo>(`${this.apiUrl}?ip=${ip}`);  
    }  
}