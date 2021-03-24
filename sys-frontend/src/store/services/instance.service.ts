import { Injectable } from '@angular/core';
import {API_INSTANCES_URL} from '../../app/commons';
import {HttpClient} from '@angular/common/http';
import {InstanceItem} from '../models/instance-item.model';
import {Store} from '@ngrx/store';
import {AddInstanceAction} from '../actions/instance.actions';
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
      // .subscribe((instanceItems: InstanceItem[]) => {
      //   this.instanceItems = instanceItems;
      //   this.storeRetrievedInstances();
      // });
  }

  // addInstance(instanceName: string, payload:  ): void {
  //   this.http.post<InstanceItem>(API_INSTANCES_URL + instanceName);
  //
  // }

  deleteInstance(instanceName: string): any {
    return this.http.delete(`${API_INSTANCES_URL}/${instanceName}`)
      .pipe(
        // TODO
      );
  }

  updateInstanceDescription(): any {

  }

  storeRetrievedInstances(): void {
    console.log(this.instanceItems); // TODO: Remove in production
    for (const instance of this.instanceItems) {
      this.store.dispatch(new AddInstanceAction(instance));
    }
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
