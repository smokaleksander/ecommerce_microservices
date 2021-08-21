import { Subjects } from '../subjects';
import { Publisher } from '../base-publisher';
import { ExpirationCompleteEvent } from '../expiration-complete-event'

export class ExpirationCompletePublisher extends Publisher<ExpirationCompleteEvent> {
  subject: Subjects.ExpirationComplete = Subjects.ExpirationComplete;
}
