import {IInstanceFilters, InstanceItem} from '../models/instance-item.model';
import {InstanceAction, InstanceActionTypes} from '../actions/instance.actions';
import {createEntityAdapter, EntityAdapter, EntityState} from '@ngrx/entity';

export interface InstanceState extends EntityState<InstanceItem>{
  selectedEntityID: number;
  loading: boolean;
  error: Error;
  filters: IInstanceFilters;
}

export function selectInstanceId(a: InstanceItem): string {
  return a.instancename;
}

export function sortByName(a: InstanceItem, b: InstanceItem): number {
  return a.instancename.localeCompare(b.instancename);
}

export const InstanceAdapter: EntityAdapter<InstanceItem> = createEntityAdapter<InstanceItem>({
  selectId: selectInstanceId,
  sortComparer: sortByName,
});

export const getSelectedInstanceId = (state: InstanceState) => state.selectedEntityID;

export const getInstanceFilters = (state: InstanceState): IInstanceFilters => state.filters;


const defaultState: InstanceState = {
  ids: [],
  entities: {},
  selectedEntityID: null,
  loading: false,
  error: undefined,
  filters: {
    searchterm: '',
    status: '',
    showOnlyOwnedInstances: false,
    showAsList: false,
    isInitialState: true
  }
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
      return InstanceAdapter.upsertMany(action.payload, {
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
      return InstanceAdapter.removeOne(action.instanceId, {
        ...state,
        error: undefined,
        loading: false
      });
    case InstanceActionTypes.DELETE_INSTANCE_FAILURE:
      return {
        ...state,
        error: action.payload,
        loading: false
      };
    case InstanceActionTypes.UPDATE_INSTANCE_FILTERS:
      return {
        ...state,
        filters: action.payload
      };
    default:
      return {...state};
  }
}

export const {
  selectAll: selectAllInstances,
  selectEntities: selectInstanceEntities,
  selectIds: selectInstanceIds,
  selectTotal: selectInstanceTotal

} = InstanceAdapter.getSelectors();
