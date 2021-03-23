import {InstanceItem} from '../models/instance-item.model';
import {InstanceAction, InstanceActionTypes} from '../actions/instance.actions';

const initialState: Array<InstanceItem> = [];

export function InstanceReducer(
  state: Array<InstanceItem> = initialState,
  action: InstanceAction
): any {
  switch (action.type) {
    case InstanceActionTypes.ADD_INSTANCE:
      return [...state, action.payload];
    default:
      return [...state];
  }
}
