import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ActivityMenuOverlayComponent } from './activity-menu-overlay.component';

describe('ActivityMenuOverlayComponent', () => {
  let component: ActivityMenuOverlayComponent;
  let fixture: ComponentFixture<ActivityMenuOverlayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ActivityMenuOverlayComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ActivityMenuOverlayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
