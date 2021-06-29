import { Action } from '@ngrx/store';
import {ApplicationGroupItem} from '../models/application-group-item.model';

export enum ApplicationGroupsActionTypes {
  LOAD_APPLICATION_GROUPS             = '[APPLICATION GROUP] Load Application Groups',
  LOAD_APPLICATION_GROUPS_SUCCESS     = '[APPLICATION GROUP] Load Application Groups Success',
  LOAD_APPLICATION_GROUPS_FAILURE     = '[APPLICATION GROUP] Load Application Groups Failure',
  FILTER_APPLICATION_GROUPS           = '[APPLICATION GROUP] Filter Application Groups'
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

export class FilterApplicationGroups implements Action {
  readonly type = ApplicationGroupsActionTypes.FILTER_APPLICATION_GROUPS;
  constructor(public payload: ApplicationGroupItem[]) {}
}


export type ApplicationGroupsAction =
  LoadApplicationGroupsAction
  | LoadApplicationGroupsSuccessAction
  | LoadApplicationGroupsFailureAction
  | FilterApplicationGroups;
