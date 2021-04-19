import { Injectable } from '@angular/core';
import {API_INSTANCES_URL} from '../../commons';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {InstanceItem} from '../models/instance-item.model';
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
    const header = new HttpHeaders();
    header.set('Content-Type', 'application/json'); // ; charset=utf-8
    return this.http.post<InstanceItem>(API_INSTANCES_URL + instanceName, JSON.parse(payload), {headers: header});
  }

  deleteInstance(instanceName: string): Observable<any> {
    return this.http.delete(API_INSTANCES_URL + instanceName);
  }

  updateInstanceDescription(instanceName: string, payload: string): Observable<JSON> {
    const header = new HttpHeaders();
    header.set('Content-Type', 'application/json'); // ; charset=utf-8
    return this.http.patch<JSON>(API_INSTANCES_URL + instanceName, JSON.parse(payload), {headers: header});
  }

  getInstanceContainerLogs(instanceName: string): Observable<JSON> {
    return this.http.get<JSON>(API_INSTANCES_URL + 'logs/' + instanceName);
  }

  manageInstance(instanceName: string, operation: string): Observable<JSON> {
    if (operation in ['start', 'stop', 'restart']) {
      return this.http.get<JSON>(API_INSTANCES_URL + operation + '/' + instanceName);
    }
    return;
  }
}
