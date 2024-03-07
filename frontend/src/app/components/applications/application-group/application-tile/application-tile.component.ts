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
  shortenDescription = false;
  showFullDescription = false;
  description = '';

  constructor(public dialog: MatDialog) { }

  @Input() application: ApplicationItem;
  @Input() searchByTag: (tag: string) => void;

  ngOnInit(): void {
    if(this.application.short_description.length > 60) {
      this.description = this.application.short_description.substring(0, 60);
      this.shortenDescription = true;
    }
    else {
      this.description = this.application.short_description;
    }
  }

  openInstallScreenDialog(): void {
    const dialogRef = this.dialog.open(InstallScreenDialogComponent, {
      data: { application: this.application, searchByTag: this.searchByTag }
    });

    // dialogRef.afterClosed().subscribe(value => {
    //   console.log(`Dialog sent: ${value}`);
    // });
  }

  toggleShowFully(e): void {
    e.stopPropagation();
    this.showFullDescription = !this.showFullDescription;

    if(this.showFullDescription) {
      this.description = this.application.short_description;
    }
    else {
      this.description = this.application.short_description.substring(0, 60);
    }
  }
}
