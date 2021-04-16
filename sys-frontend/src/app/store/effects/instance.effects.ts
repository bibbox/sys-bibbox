import {Injectable} from '@angular/core';
import {Actions, createEffect, ofType} from '@ngrx/effects';
import {
  InstanceActionTypes,
  AddInstanceAction, AddInstanceFailureAction, AddInstanceSuccessAction,
  LoadInstancesAction, LoadInstancesFailureAction, LoadInstancesSuccessAction,
  DeleteInstanceAction, DeleteInstanceFailureAction, DeleteInstanceSuccessAction
} from '../actions/instance.actions';
import {catchError, map, mergeMap} from 'rxjs/operators';
import {InstanceService} from '../services/instance.service';
import {of} from 'rxjs';

@Injectable()
export class InstanceEffects {

  loadInstances$ =  createEffect(() =>
    this.actions$.pipe(
      ofType<LoadInstancesAction>(InstanceActionTypes.LOAD_INSTANCES),
      mergeMap(
        () => this.instanceService.getInstances()
          .pipe(
            map(data => new LoadInstancesSuccessAction(data)),
            catchError(error => of(new LoadInstancesFailureAction(error)))
          )
      )
    )
  );
  addInstance$ = createEffect(() =>
    this.actions$.pipe(
      ofType<AddInstanceAction>(InstanceActionTypes.ADD_INSTANCE),
      mergeMap(
        (action) =>
          this.instanceService.postInstance(action.instanceName, action.payload) // TODO: correct parameters
          .pipe(
            map(data => new AddInstanceSuccessAction(data)),
            catchError(error => of(new AddInstanceFailureAction(error)))
          )
      )
    )
  );
  deleteInstance$ = createEffect(() =>
    this.actions$.pipe(
      ofType<DeleteInstanceAction>(InstanceActionTypes.DELETE_INSTANCE),
      mergeMap(
        (action) => this.instanceService.deleteInstance(action.instanceId) // TODO: correct parameters
          .pipe(
            map(data => new DeleteInstanceSuccessAction(action.instanceId)),
            catchError(error => of(new DeleteInstanceFailureAction(error)))
          )
      )
    )
  );

  constructor(private actions$: Actions, private instanceService: InstanceService) {

  }

}
