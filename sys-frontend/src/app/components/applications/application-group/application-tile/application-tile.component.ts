import {Component, Input, OnInit} from '@angular/core';
import {ApplicationItem} from '../../../../store/models/application-group-item.model';
import {MatDialog} from '@angular/material/dialog';
import {InstallScreenDialogComponent} from '../../install-screen-dialog/install-screen-dialog.component';

@Component({
  selector: 'app-application-tile',
  templateUrl: './application-tile.component.html',
  styleUrls: ['./application-tile.component.scss']
})
export class ApplicationTileComponent implements OnInit {

  constructor(public dialog: MatDialog) { }

  @Input() application: ApplicationItem;

  ngOnInit(): void {
  }

  openInstallScreenDialog(): void {
    console.log(this.application);
    const dialogRef = this.dialog.open(InstallScreenDialogComponent, {data: {application: this.application}});

    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });

    console.log(this.application);
    // TODO
  }

}
