import { Action } from '@ngrx/store';
import {ApplicationGroupItem} from '../models/application-group-item.model';

export enum ApplicationGroupsActionTypes {
  LOAD_APPLICATION_GROUPS             = '[APPLICATON GROUP] Load Application Groups',
  LOAD_APPLICATION_GROUPS_SUCCESS     = '[APPLICATON GROUP] Load Application Groups Success',
  LOAD_APPLICATION_GROUPS_FAILURE     = '[APPLICATON GROUP] Load Application Groups Failure',
  // LOAD_APPLICATION_APPINFO            = '[APPLICATION] Load AppInfo of Application',
  // LOAD_APPLICATION_APPINFO_SUCCESS    = '[APPLICATION] Load AppInfo of Application Success',
  // LOAD_APPLICATION_APPINFO_FAILURE    = '[APPLICATION] Load AppInfo of Application Failure',
  // LOAD_APPLICATION_ENVPARAMS          = '[APPLICATION] Load Environment Parameters of Application',
  // LOAD_APPLICATION_ENVPARAMS_SUCCESS  = '[APPLICATION] Load Environment Parameters of Application Success',
  // LOAD_APPLICATION_ENVPARAMS_FAILURE  = '[APPLICATION] Load Environment Parameters of Application Failure',
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
//
// export class LoadAppinfoAction implements Action {
//   readonly type = ApplicationGroupsActionTypes.LOAD_APPLICATION_APPINFO;
// }
//
// export class LoadAppinfoSuccessAction implements Action {
//   readonly type = ApplicationGroupsActionTypes.LOAD_APPLICATION_APPINFO_SUCCESS;
//   constructor(public appGroup: ApplicationGroupItem, public appItem: ApplicationItem, public appinfo: AppInfo) {}
// }
//
// export class LoadAppinfoFailureAction implements Action {
//   readonly type = ApplicationGroupsActionTypes.LOAD_APPLICATION_APPINFO_FAILURE;
//   constructor(public appGroup: ApplicationGroupItem, public appItem: ApplicationItem, public payload: Error) {}
// }
//
// export class LoadEnvparamAction implements Action {
//   readonly type = ApplicationGroupsActionTypes.LOAD_APPLICATION_ENVPARAMS;
// }
//
// export class LoadEnvparamSuccessAction implements Action {
//   readonly type = ApplicationGroupsActionTypes.LOAD_APPLICATION_ENVPARAMS_SUCCESS;
//   constructor(public appGroup: ApplicationGroupItem, public appItem: ApplicationItem, public envparams: EnvironmentParameters[]) {}
// }
//
// export class LoadEnvparamFailureAction implements Action {
//   readonly type = ApplicationGroupsActionTypes.LOAD_APPLICATION_ENVPARAMS_FAILURE;
//   constructor(public appGroup: ApplicationGroupItem, public appItem: ApplicationItem, public payload: Error) {}
// }


export type ApplicationGroupsAction =
  LoadApplicationGroupsAction
  | LoadApplicationGroupsSuccessAction
  | LoadApplicationGroupsFailureAction;
  // | LoadAppinfoAction
  // | LoadAppinfoSuccessAction
  // | LoadAppinfoFailureAction
  // | LoadEnvparamAction
  // | LoadEnvparamSuccessAction
  // | LoadEnvparamFailureAction;
