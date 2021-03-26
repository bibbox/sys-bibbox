import { Injectable } from '@angular/core';
import {API_INSTANCES_URL} from '../../commons';
import {HttpClient} from '@angular/common/http';
import {InstanceItem} from '../models/instance-item.model';
import {Store} from '@ngrx/store';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class InstanceService {

  instanceItems: InstanceItem[];

  constructor(
    private http: HttpClient,
    private store: Store<{AppState}>) { }

  loadInstances(): Observable<InstanceItem[]>{
    return this.http.get<InstanceItem[]>(API_INSTANCES_URL);
  }

  addInstance(instanceName: string, payload: JSON): Observable<InstanceItem> {
    return this.http.post<InstanceItem>(API_INSTANCES_URL + instanceName, payload);
  }

  deleteInstance(instanceName: string): Observable<any> {
    return this.http.delete(API_INSTANCES_URL + instanceName)
      .pipe(
        // TODO
      );
  }

  updateInstanceDescription(instanceName: string, shortDescr: string, longDescr: string): Observable<InstanceItem> {
    return this.http.patch<InstanceItem>(API_INSTANCES_URL + instanceName, {short_description: shortDescr, long_description: longDescr});
  }


  // getInstanceByID() {
  // }
  //
  // postInstance() {
  //
  // }
  //
  // deleteInstanceByID {
  //
  // }
}
