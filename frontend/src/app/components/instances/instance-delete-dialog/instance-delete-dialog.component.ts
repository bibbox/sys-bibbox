import { Store } from '@ngrx/store';
import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialog} from '@angular/material/dialog';
import { DeleteInstanceAction } from '../../../store/actions/instance.actions';
import { AppState } from '../../../store/models/app-state.model';


@Component({
  selector: 'app-instance-delete-dialog',
  templateUrl: './instance-delete-dialog.component.html',
  styleUrls: ['./instance-delete-dialog.component.scss']
})
export class InstanceDeleteDialogComponent implements OnInit {

  instanceName: string;

  constructor(
    @Inject(MAT_DIALOG_DATA) public props: string,
    private store: Store<AppState>,
    private dialog: MatDialog
  ) {
    this.instanceName = props;
  }

  ngOnInit(): void {
  }

  confirmDelete(): void {
    this.store.dispatch(new DeleteInstanceAction(this.instanceName));
    this.closeDialog();
  }

  closeDialog = () => {
    this.dialog?.closeAll();
  }
}
