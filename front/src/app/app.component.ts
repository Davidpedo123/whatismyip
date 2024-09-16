import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { IpGetSComponent } from "./componentes/ipget/ipget.component";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, IpGetSComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'whatismyip-front';
}
