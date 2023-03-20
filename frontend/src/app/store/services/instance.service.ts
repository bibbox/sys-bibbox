import { Injectable } from '@angular/core';
import {API_INSTANCES_URL} from '../../commons';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {InstanceItem} from '../models/instance-item.model';
import {Observable, of} from 'rxjs';
import {map} from 'rxjs/operators';
import {DeleteAllInstancesAction, LoadInstancesAction} from '../actions/instance.actions';
import {Store} from '@ngrx/store';
import {AppState} from '../models/app-state.model';

@Injectable({
  providedIn: 'root'
})
export class InstanceService {

  instanceItems: InstanceItem[];

  constructor(private http: HttpClient, private store: Store<AppState>) {
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
    return this.http.post<InstanceItem>(API_INSTANCES_URL + instanceName, JSON.parse(payload), {headers: header})
      .pipe(map((result: any) => result.instance));
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

  checkIfInstanceExists(instanceName: string): Observable<string> {
    return this.http.get<string>(API_INSTANCES_URL + 'names/' + instanceName);
  }

  manageInstance(instanceName: string, operation: string): Observable<any> {
    if (['start', 'stop', 'restart'].includes(operation)) {
      return this.http.get<JSON>(API_INSTANCES_URL + operation + '/' + instanceName);
    }
    else {
      console.log('operation not supported');
      return of('operation not supported');
    }
  }

  refreshStoreInstances(): void {
    // this.store.dispatch(new DeleteAllInstancesAction());
    this.store.dispatch(new LoadInstancesAction());
  }
}
