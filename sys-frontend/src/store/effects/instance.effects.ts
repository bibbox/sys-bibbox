import {Injectable} from '@angular/core';
import {Actions, createEffect, ofType, Effect} from '@ngrx/effects';
import {
  InstanceActionTypes,
  LoadInstancesAction,
  LoadInstancesFailureAction,
  LoadInstancesSuccessAction
} from '../actions/instance.actions';
import {catchError, map, mergeMap} from 'rxjs/operators';
import {InstanceService} from '../services/instance.service';
import {of} from 'rxjs';

@Injectable()
export class InstanceEffects {

  loadInstances$ = // createEffect(() =>
    this.actions$.pipe(
      ofType<LoadInstancesAction>(InstanceActionTypes.LOAD_INSTANCES),
      mergeMap(
        () => this.instanceService.loadInstances()
          .pipe(
            map(data => new LoadInstancesSuccessAction(data)),
            catchError(error => of(new LoadInstancesFailureAction(error)))
          )
      )
    );

  constructor(private actions$: Actions, private instanceService: InstanceService) {

  }

}
