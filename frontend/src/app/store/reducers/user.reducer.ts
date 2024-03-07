import {createEntityAdapter, EntityAdapter, EntityState} from '@ngrx/entity';
import {UserRepresentation, IUserFilters} from '../models/user.model';
import {UserAction, UserActionTypes} from '../actions/user.actions';


export interface UserState extends EntityState<UserRepresentation>{
  selectedEntityID: number;
  loading: boolean;
  error: Error;
  filters: IUserFilters;
}

export const UserAdapter: EntityAdapter<UserRepresentation> = createEntityAdapter<UserRepresentation>({
  selectId: (user: UserRepresentation) => user.id,
});

//
// export const getSelectedUserId = (state: UserState) => null; // not needed anywhere but required by the selector


const defaultState: UserState = {
  ids: [],
  entities: {},
  selectedEntityID: null,
  loading: false,
  error: undefined,
  filters: {
    searchterm: '',
    role: ''
  }
};

export function sortByName(a: UserRepresentation, b: UserRepresentation): number {
  return a.username.localeCompare(b.username);
}

export const initialState = UserAdapter.getInitialState(defaultState);

export const getUserFilters = (state: UserState): IUserFilters => state.filters;

export function UserReducer(
  state: UserState = defaultState,
  action: UserAction
): any {
  switch (action.type) {
    case UserActionTypes.LOAD_USERS:
      return {
        ...state,
        loading: true
      };
    case UserActionTypes.LOAD_USERS_SUCCESS:
      return UserAdapter.upsertMany(action.payload, {
        ...state,
        loading: false,
        error: undefined
      });
    case UserActionTypes.LOAD_USERS_FAILURE:
      return {
        ...state,
        error: action.payload,
        loading: false
      };
    case UserActionTypes.CREATE_USER:
      return {
        ...state,
        loading: true
      };
    case UserActionTypes.CREATE_USER_SUCCESS:
      return UserAdapter.upsertOne(action.payload.userRepresentation, {
        ...state,
        loading: false,
      });
    case UserActionTypes.CREATE_USER_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload
      }
    case UserActionTypes.UPDATE_USER_ROLE_MAPPINGS:
      return {
        ...state,
        loading: true
      }
    case UserActionTypes.UPDATE_USER_ROLE_MAPPINGS_SUCCESS:
      return UserAdapter.upsertMany(action.payload.users, {
        ...state,
        loading: false,
      });

    case UserActionTypes.UPDATE_USER_ROLE_MAPPINGS_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload
      }

    case UserActionTypes.DELETE_USER:
      return {
        ...state,
        loading: true
      }
    case UserActionTypes.DELETE_USER_SUCCESS:
      return UserAdapter.removeOne(action.payload.userID, {
        ...state,
        loading: false,
      });
    case UserActionTypes.DELETE_USER_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload
      }
    case UserActionTypes.UPDATE_USER_FILTERS:
      return {
        ...state,
        filters: action.payload
      };
    default:
      return {...state};
  }
}

export const {
  selectAll: selectAllUsers,
  selectEntities: selectUserEntities,
  // selectIds: selectUserIds,
  selectTotal: selectUserTotal,
} = UserAdapter.getSelectors();
