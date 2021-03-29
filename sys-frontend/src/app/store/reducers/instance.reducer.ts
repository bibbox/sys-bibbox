import {InstanceItem} from '../models/instance-item.model';
import {InstanceAction, InstanceActionTypes} from '../actions/instance.actions';

export interface InstanceState {
  list: InstanceItem[];
  loading: boolean;
  error: Error;
}

const initialState: InstanceState = {
  list: [],
  loading: false,
  error: undefined
};

export function InstanceReducer(
  state: InstanceState = initialState,
  action: InstanceAction
): any {
  switch (action.type) {
    case InstanceActionTypes.LOAD_INSTANCES:
      return {
        ...state,
        loading: true
      };
    case InstanceActionTypes.LOAD_INSTANCES_SUCCESS:
      return {
        ...state,
        list: action.payload,
        loading: false,
        error: undefined
      };
    case InstanceActionTypes.LOAD_INSTANCES_FAILURE:
      return {
        ...state,
        error: action.payload,
        loading: false
      };
    case InstanceActionTypes.ADD_INSTANCE:
      return {
        ...state,
        loading: true
      };
    case InstanceActionTypes.ADD_INSTANCE_SUCCESS:
      return {
        ...state,
        list: [...state.list, action.payload],
        loading: false,
        error: undefined
      };
    case InstanceActionTypes.ADD_INSTANCE_FAILURE:
      return {
        ...state,
        error: action.payload,
        loading: false
      };
    case InstanceActionTypes.DELETE_INSTANCE:
      return {
        ...state,
        loading: true
      };
    case InstanceActionTypes.DELETE_INSTANCE_SUCCESS:
      return {
        ...state,
        list: state.list.filter(item => item.instancename !== action.payload),
        loading: false,
        error: undefined
      };
    case InstanceActionTypes.DELETE_INSTANCE_FAILURE:
      return {
        ...state,
        error: action.payload,
        loading: false
      };
    default:
      return {...state};
  }
}
