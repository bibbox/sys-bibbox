import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';
import {API_KEYVALUE_URL} from '../../commons';
import { KeyValueItem } from '../models/keyvalue.model';

@Injectable({
  providedIn: 'root'
})
export class KeyValueService {

  constructor(private http: HttpClient) { }

  getValueByKey(key: string): Observable<KeyValueItem | null> {
    return this.http.get<KeyValueItem>(API_KEYVALUE_URL + key);
  }

  updateValueByKey(key: string, value: KeyValueItem): Observable<KeyValueItem> {
    const header = new HttpHeaders();
    header.set('Content-Type', 'application/json'); // ; charset=utf-8
    return this.http.put<any>(API_KEYVALUE_URL + key, value, {headers: header});
  }
}
