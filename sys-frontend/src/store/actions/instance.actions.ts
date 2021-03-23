import {Action} from '@ngrx/store';
import {InstanceItem} from '../models/instance-item.model';

export enum InstanceActionTypes {
  LOAD_INSTANCES = '[INSTANCE] Load Instances',
  LOAD_INSTANCES_SUCCESS = '[INSTANCE] Load Instance Success',
  LOAD_INSTANCES_FAILURE = '[INSTANCE] Load Instance Failure',
  ADD_INSTANCE = '[INSTANCE] Add Instance',
  ADD_INSTANCE_SUCCESS = '[INSTANCE] Add Instance Success',
  ADD_INSTANCE_FAILURE = '[INSTANCE] Add Instance Failure',
  DELETE_INSTANCE = '[INSTANCE] Delete Instance',
  DELETE_INSTANCE_SUCCESS = '[INSTANCE] Delete Instance Success',
  DELETE_INSTANCE_FAILURE = '[INSTANCE] Delete Instance Failure'
}

export class LoadInstanceAction implements Action {
  readonly type = InstanceActionTypes.LOAD_INSTANCES;
}

export class LoadInstanceSuccessAction implements Action {
  readonly type = InstanceActionTypes.LOAD_INSTANCES_SUCCESS;

  constructor(public payload: Array<InstanceItem>) {}
}

export class LoadInstanceFailureAction implements Action {
  readonly type = InstanceActionTypes.LOAD_INSTANCES_FAILURE;

  constructor(public payload: Error) {}
}

export class AddInstanceAction implements Action {
  readonly type = InstanceActionTypes.ADD_INSTANCE;

  constructor(public payload: InstanceItem) {}
}

export type InstanceAction =
  LoadInstanceAction
  | LoadInstanceSuccessAction
  | LoadInstanceFailureAction
  | AddInstanceAction; // | DeleteInstanceAction | ...
