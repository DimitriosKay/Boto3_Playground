class destroy_VPC:

    def __init__(self, resource):
        self._resource = resource

    def vpc_id(self, filters):
        return self._resource.meta.client.describe_vpcs(
            Filters=filters
        )
    
    def detach_igw(self, igw_id):
        print ('Detaching Gateway ...')
        return self._resource.detach_internet_gateway(
            InternetGatewayId=igw_id
        )

    def instance_id(self):
        return self._resource.instances.all()

    def waiter(self, instance_id):
        return self._resource.meta.client.get_waiter('instance_terminated')

    '''
    # where I was trying to create a lowkey waiter
    # issue - couldnt re-assign the status value in the while loop checker
    # making it repeat only the initial state
    def describe_instance_status(self, instance_id):
        instance_status = self._resource.meta.client.describe_instance_status(
            InstanceIds=[instance_id]
        )

        for statuses in instance_status['InstanceStatuses']:
            #print (statuses)
            #print (str(type(statuses)) + ' :statuses')
            instance_state = statuses['InstanceState']['Name']
            #print (statuses['InstanceState'])

            if type(instance_state) is type(None):
                print ('None-aroony')
                instance_state = 'stopped'
                return instance-state
            #print (instance_state + ' ' + instance_id)
            else:
                print (instance_state + ' ' + instance_id)
                return instance_state
    '''
