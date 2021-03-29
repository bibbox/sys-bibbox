import { Action } from '@ngrx/store';
import {ApplicationGroupItem} from '../models/application-group-item.model';

export enum ApplicationGroupActionTypes {
  LOAD_APPLICATION_GROUP          = '[APPLICATON] Load Application Group',
  LOAD_APPLICATION_GROUP_SUCCESS  = '[APPLICATON] Load Application Group Success',
  LOAD_APPLICATION_GROUP_FAILURE  = '[APPLICATON] Load Application Group Failure',
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
  LoadApplicationGroupAction
  | LoadApplicationGroupSuccessAction
  | LoadApplicationGroupFailureAction;
