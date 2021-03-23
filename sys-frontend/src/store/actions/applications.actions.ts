import { Action } from '@ngrx/store';
import {ApplicationGroupItem} from '../models/application-group-item.model';

export enum ApplicationGroupActionTypes {
  ADD_APPLICATION_GROUP = '[APPLICATION] Add Application Group',
  GET_APPLICATIONS = '[APPLICATION] Get Applications from API',
}

export class AddApplicationGroupAction implements Action {
  readonly type = ApplicationGroupActionTypes.ADD_APPLICATION_GROUP;

  constructor(public payload: ApplicationGroupItem) {}
}
export type ApplicationGroupAction = AddApplicationGroupAction;
