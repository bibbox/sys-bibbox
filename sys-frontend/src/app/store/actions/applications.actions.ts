import { Action } from '@ngrx/store';
import {ApplicationGroupItem} from '../models/application-group-item.model';

export enum ApplicationGroupsActionTypes {
  LOAD_APPLICATION_GROUPS          = '[APPLICATON GROUP] Load Application Groups',
  LOAD_APPLICATION_GROUPS_SUCCESS  = '[APPLICATON GROUP] Load Application Groups Success',
  LOAD_APPLICATION_GROUPS_FAILURE  = '[APPLICATON GROUP] Load Application Groups Failure',
}

export class LoadApplicationGroupsAction implements Action {
  readonly type = ApplicationGroupsActionTypes.LOAD_APPLICATION_GROUPS;
}

export class LoadApplicationGroupsSuccessAction implements Action {
  readonly type = ApplicationGroupsActionTypes.LOAD_APPLICATION_GROUPS_SUCCESS;

  constructor(public payload: ApplicationGroupItem[]) {}
}

export class LoadApplicationGroupsFailureAction implements Action {
  readonly type = ApplicationGroupsActionTypes.LOAD_APPLICATION_GROUPS_FAILURE;

  constructor(public payload: Error) {}
}
export type ApplicationGroupsAction =
  LoadApplicationGroupsAction
  | LoadApplicationGroupsSuccessAction
  | LoadApplicationGroupsFailureAction;
