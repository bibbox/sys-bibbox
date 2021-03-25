import { Action } from '@ngrx/store';
import {ApplicationGroupItem} from '../models/application-group-item.model';

export enum ApplicationGroupActionTypes {
  ADD_APPLICATION_GROUP = '[APPLICATION] Add Application Group',
  LOAD_APPLICATION_GROUP = '[APPLICATON] Load Application Group',
  LOAD_APPLICATION_GROUP_SUCCESS = '[APPLICATON] Load Application Group Success',
  LOAD_APPLICATION_GROUP_FAILURE = '[APPLICATON] Load Application Group Failure',
}

export class AddApplicationGroupAction implements Action {
  readonly type = ApplicationGroupActionTypes.ADD_APPLICATION_GROUP;

  constructor(public payload: ApplicationGroupItem) {}
}

export class LoadApplicationGroupAction implements Action {
  readonly type = ApplicationGroupActionTypes.LOAD_APPLICATION_GROUP;
}

export class LoadApplicationGroupSuccessAction implements Action {
  readonly type = ApplicationGroupActionTypes.LOAD_APPLICATION_GROUP_SUCCESS;

  constructor(public payload: Array<ApplicationGroupItem>) {}
}

export class LoadApplicationGroupFailureAction implements Action {
  readonly type = ApplicationGroupActionTypes.LOAD_APPLICATION_GROUP_FAILURE;

  constructor(public payload: Error) {}
}
export type ApplicationGroupAction =
  AddApplicationGroupAction
  | LoadApplicationGroupAction
  | LoadApplicationGroupSuccessAction
  | LoadApplicationGroupFailureAction;
