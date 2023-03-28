import { Text, Card, RingProgress, Badge } from '@mantine/core';
import { useStyles } from '../../styles';

interface StatsRingCardProps {
  title: string;
  completed: number;
  total: number;
  rateLimit: number;
  ratePeriod: number;
}

export function ProjectStats({ title, completed, total, rateLimit, ratePeriod }: StatsRingCardProps) {
  const { classes, theme } = useStyles();

  return (
    <Card withBorder p="xl" radius="md" className={classes.card}>
      <div className={classes.inner}>
        <div>
          <Text fz="xl" className={classes.label}>
            {title}
          </Text>
          <div>
            <Text className={classes.lead} mt={30}>
              {completed.toLocaleString()} <Badge>reqs</Badge>
            </Text>
            <Text fz="xs" color="dimmed">
              Completed this month
            </Text>
            <Text className={classes.lead} mt={30}>
              {total.toLocaleString()} <Badge>reqs</Badge>
            </Text>
            <Text fz="xs" color="dimmed">
              Total per month
            </Text>
            <Text className={classes.lead} mt={30}>
              {rateLimit} per {ratePeriod} second(s)
            </Text>
            <Text fz="xs" color="dimmed">
              Rate limit
            </Text>
          </div>
        </div>

        <div className={classes.ring}>
          <RingProgress
            roundCaps
            thickness={6}
            size={150}
            sections={[{ value: (completed / total) * 100, color: theme.primaryColor }]}
            label={
              <div>
                <Text ta="center" fz="lg" className={classes.label}>
                  {((completed / total) * 100).toFixed(1)}%
                </Text>
                <Text ta="center" fz="xs" c="dimmed">
                  Completed
                </Text>
              </div>
            }
          />
        </div>
      </div>
    </Card>
  );
}