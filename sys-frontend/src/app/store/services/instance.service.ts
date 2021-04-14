import { Injectable } from '@angular/core';
import {API_INSTANCES_URL} from '../../commons';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {InstanceItem} from '../models/instance-item.model';
import {Store} from '@ngrx/store';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class InstanceService {

  instanceItems: InstanceItem[];

  constructor(private http: HttpClient) {
  }

  getInstances(): Observable<InstanceItem[]>{
    return this.http.get<InstanceItem[]>(API_INSTANCES_URL);
  }

  getInstanceById(id: string): Observable<InstanceItem>{
    return this.http.get<InstanceItem>(API_INSTANCES_URL + id);
  }

  postInstance(instanceName: string, payload: string): Observable<InstanceItem> {
    const headers = new HttpHeaders();
    headers.set('Content-Type', 'application/json; charset=utf-8');
    return this.http.post<InstanceItem>(API_INSTANCES_URL + instanceName, payload, {headers});
  }

  deleteInstance(instanceName: string): Observable<any> {
    return this.http.delete(API_INSTANCES_URL + instanceName);
  }

  updateInstanceDescription(instanceName: string, shortDescr: string, longDescr: string): Observable<InstanceItem> {
    return this.http.patch<InstanceItem>(API_INSTANCES_URL + instanceName, {short_description: shortDescr, long_description: longDescr});
  }
}
