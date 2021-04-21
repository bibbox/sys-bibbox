import {Injectable} from '@angular/core';
import {Actions, createEffect, ofType} from '@ngrx/effects';
import {catchError, map, mergeMap} from 'rxjs/operators';
import {of} from 'rxjs';
import {ApplicationService} from '../services/application.service';
import {
  ApplicationGroupsActionTypes,
  LoadApplicationGroupsAction, LoadApplicationGroupsFailureAction, LoadApplicationGroupsSuccessAction
} from '../actions/applications.actions';

@Injectable()
export class ApplicationsEffects {

  loadApplicationGroups$ =  createEffect(() =>
    this.actions$.pipe(
      ofType<LoadApplicationGroupsAction>(ApplicationGroupsActionTypes.LOAD_APPLICATION_GROUPS),
      mergeMap(
        () => this.applicationService.loadApplications()
          .pipe(
            map(data => new LoadApplicationGroupsSuccessAction(data)),
            catchError(error => of(new LoadApplicationGroupsFailureAction(error)))
          )
      )
    )
  );

  constructor(private actions$: Actions, private applicationService: ApplicationService) {
  }

}
