import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApplicationTileComponent } from './application-tile.component';

describe('ApplicationTileComponent', () => {
  let component: ApplicationTileComponent;
  let fixture: ComponentFixture<ApplicationTileComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ApplicationTileComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ApplicationTileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
