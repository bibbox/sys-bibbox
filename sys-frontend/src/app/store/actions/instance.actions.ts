import {Action} from '@ngrx/store';
import {InstanceItem} from '../models/instance-item.model';

export enum InstanceActionTypes {
  LOAD_INSTANCES = '[INSTANCE] Load Instances',
  LOAD_INSTANCES_SUCCESS = '[INSTANCE] Load Instances Success',
  LOAD_INSTANCES_FAILURE = '[INSTANCE] Load Instances Failure',
  ADD_INSTANCE = '[INSTANCE] Add Instance',
  ADD_INSTANCE_SUCCESS = '[INSTANCE] Add Instance Success',
  ADD_INSTANCE_FAILURE = '[INSTANCE] Add Instance Failure',
  DELETE_INSTANCE = '[INSTANCE] Delete Instance',
  DELETE_INSTANCE_SUCCESS = '[INSTANCE] Delete Instance Success',
  DELETE_INSTANCE_FAILURE = '[INSTANCE] Delete Instance Failure'
}

export class LoadInstancesAction implements Action {
  readonly type = InstanceActionTypes.LOAD_INSTANCES;
}

export class LoadInstancesSuccessAction implements Action {
  readonly type = InstanceActionTypes.LOAD_INSTANCES_SUCCESS;

  constructor(public payload: InstanceItem[]) {}
}

export class LoadInstancesFailureAction implements Action {
  readonly type = InstanceActionTypes.LOAD_INSTANCES_FAILURE;

  constructor(public payload: Error) {}
}

export class AddInstanceAction implements Action {
  readonly type = InstanceActionTypes.ADD_INSTANCE;

  constructor(public payload: InstanceItem) {}
}

export class AddInstanceSuccessAction implements Action {
  readonly type = InstanceActionTypes.ADD_INSTANCE_SUCCESS;

  constructor(public payload: InstanceItem) {}
}

export class AddInstanceFailureAction implements Action {
  readonly type = InstanceActionTypes.ADD_INSTANCE_FAILURE;

  constructor(public payload: Error) {}
}

export class DeleteInstanceAction implements Action {
  readonly type = InstanceActionTypes.DELETE_INSTANCE;

  constructor(public payload: string) {}
}

export class DeleteInstanceSuccessAction implements Action {
  readonly type = InstanceActionTypes.DELETE_INSTANCE_SUCCESS;

  constructor(public payload: string) {}
}

export class DeleteInstanceFailureAction implements Action {
  readonly type = InstanceActionTypes.DELETE_INSTANCE_FAILURE;

  constructor(public payload: Error) {}
}



export type InstanceAction =
  LoadInstancesAction
  | LoadInstancesSuccessAction
  | LoadInstancesFailureAction
  | AddInstanceAction
  | AddInstanceSuccessAction
  | AddInstanceFailureAction
  | DeleteInstanceAction
  | DeleteInstanceSuccessAction
  | DeleteInstanceFailureAction;
