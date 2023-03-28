import { Group, Anchor } from '@mantine/core';
import logo from '../assets/images/logo.svg';
import { useStyles } from '../styles';


export function Logo({ size } : {size: number}) {
  const { classes } = useStyles();

  return (
    <Group>
      <img src={logo} alt="logo" width={size} height={size} />
      <Anchor href="/" size="lg" className={classes.logo}>Tronql</Anchor>
    </Group>
  );
}