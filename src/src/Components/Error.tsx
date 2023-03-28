import { startsWith, trim } from 'lodash';

import { Alert } from '@mantine/core';
import { IconAlertCircle } from '@tabler/icons';


export function Error({ text } : { text : string | undefined }) {
  if (! text) {
    return null;
  }

  if (startsWith(text, 'ApolloError:')) {
    text = text.substring(12)
  }
  text = trim(text);

  return (
    <Alert mt="xl" mb="xl" icon={<IconAlertCircle size={16} />} title="Error" color="red">{text}</Alert>
  )
}
