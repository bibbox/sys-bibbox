import {InstanceItem} from '../models/instance-item.model';
import {InstanceAction, InstanceActionTypes} from '../actions/instance.actions';
import {createEntityAdapter, EntityAdapter, EntityState} from '@ngrx/entity';

export interface InstanceState extends EntityState<InstanceItem>{
  selectedEntityID: number | null;
  loading: boolean;
  error: Error;
}

export const InstanceAdapter: EntityAdapter<InstanceItem> = createEntityAdapter<InstanceItem>({
  selectId: (a: InstanceItem) => a.instancename,
});

const defaultState: InstanceState = {
  ids: [],
  entities: {},
  selectedEntityID: null,
  loading: false,
  error: undefined
};

export const initialState = InstanceAdapter.getInitialState(defaultState);

export function InstanceReducer(
  state: InstanceState = defaultState,
  action: InstanceAction
): any {
  switch (action.type) {
    case InstanceActionTypes.LOAD_INSTANCES:
      return {
        ...state,
        loading: true
      };
    case InstanceActionTypes.LOAD_INSTANCES_SUCCESS:
      return InstanceAdapter.addMany(action.payload, {
        ...state,
        loading: false,
        error: undefined
      });
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
      return InstanceAdapter.addOne(action.payload, {
        ...state,
        loading: false,
        error: undefined
      });
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
      return InstanceAdapter.removeOne(action.payload, {
        ...state,
        loading: false,
        error: undefined
      });
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
