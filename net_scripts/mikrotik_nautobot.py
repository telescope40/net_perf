#Louis DeVictoria
# Script to pull address / nat from cloud-fws and update nautobot
from nautobot.dcim.models import Device, Interface
from django.contrib.contenttypes.models import ContentType
from nautobot.ipam.models import IPAddress, Device, Interface , Status , VLAN
from nautobot.extras.models import Status
from nautobot.extras.jobs import *
from nautobot.extras.jobs import Job, StringVar, MultiObjectVar
from nautobot.extras.models.secrets import Secret
import routeros_api
import ipaddress
import socket

name = "Firewall Jobs"

#Version 1.1 Public DNS , Internal DNS , Interfaces
##TODO Write Prefixes for all internal Subnets
##TODO Tie in the vlans to the prefixes
##TODO Get Or Create VlanGroup and Add Objects
## Internal vs External DNS indication in the records in Nautobot


class Mikrotik_Sync(Job):

    class Meta:
        name = "Mikrtotik SYNC "
        description = "Mikrotik SYNC "
        field_order = ['device']

    device = MultiObjectVar(
            model=Device,
            query_params={
                'status': 'active',
                'role':'cloud-fw'
            }
    )
    def _conn_mt(self,host):
        username = Secret.objects.get(slug="cloudfw_username").get_value()
        fwuser=username
        password = Secret.objects.get(slug="cloudfw_password").get_value()
        fwpassword=password
        #Secure API
        connection = routeros_api.RouterOsApiPool(host, username=fwuser, password=fwpassword, plaintext_login=True, use_ssl=True, ssl_verify=False ,ssl_verify_hostname=True,)
        api = connection.get_api()
        return api

    def _get_intfs(self,host):
        api = self._conn_mt(host)
    ## Get Interfaces ##
        int_api = api.get_resource("/interface")
        all_interfaces = int_api.get()
        self.log_success(obj=all_interfaces, message="Get Interfaces")
        return all_interfaces


    def _add_intfs(self,host,all_interfaces):
        ## Get Device UUID ##
        dev_uuid = self._get_dev_uuid(host)
        for x in all_interfaces:
                comment = x.get('comment')
                name = x['name']
                id = x['id']
                mac = x.get('mac-address','C4:AD:34:00:00:00')
                type = x['type']
                untagged_vlan_id = None
                ethernet_int = self._write_int(dev_uuid,mac,type,name,untagged_vlan_id)
                result = f"name:{name}, id:{id}, mac:{mac}, comment:{comment}"
                self.log_success(obj=result, message="One of the interfaces")

    ## Get Vlans ##
    def _get_vlans(self,host):
        api = self._conn_mt(host)
        vlans = api.get_resource("/interface/vlan")
        all_vlans = vlans.get()
        self.log_success(obj=all_vlans, message="Got Vlans")
        return all_vlans

    def _add_vlans(self,all_vlans,status,siteid,dev_uuid):
        for y in all_vlans:
                comment = y.get('comment')
                name = y['name']
                id = y['id']
                vlan = y['vlan-id']
                mac = y.get('mac-address','C4:AD:34:00:00:00')
                vlan_int = self._write_vlan(vlan,status,name,siteid)
                result = f"name:{name}, id:{id}, mac:{mac}, comment:{comment}"
                self.log_success(obj=vlan_int, message="Added Vlans")
                return vlan_int

        for y in all_vlans:
                comment = y.get('comment')
                name = y['name']
                id = y['id']
                vlan = y['vlan-id']
                mac_address = y.get('mac-address','C4:AD:34:00:00:00')
                vlan_uuid = VLAN.objects.get(vid=vlan,site=siteid)
                untagged_vlan_id = vlan_uuid.id
                vlan_intfs = self._write_int(dev_uuid,mac_address,type,name,untagged_vlan_id)
                self.log_success(obj=vlan_intfs, message="Added Interface Vlans")
                return vlan_intfs

    def _is_private(self,address):
        result = ipaddress.IPv4Interface(address).is_private
        return result


    ## Get NAT ##
    def _get_nats(self,host):
        api = self._conn_mt(host)
        nat = api.get_resource("/ip/firewall/nat/")
        all_nats = nat.get()
        self.log_success(obj=all_nats, message="Get NATs")
        return all_nats

    def _get_static_nat(self,host,address):
        try:
            api = self._conn_mt(host)
            nat = api.get_resource("/ip/firewall/nat")
            src_nat = (nat.get(action='dst-nat',dst_address=address)[0]['to-addresses'])
            self.log_success(obj=src_nat, message="Get Inside NAT")
            return src_nat
        except:
            return None

    def _add_nats(self,host,all_nats,status):
        dev_uuid = self._get_dev_uuid(host)
        for x in all_nats:
            if x.get('action') == 'src-nat' and x.get('src-address') != None:
                address = x.get('src-address')
                status = status
                comment = x.get('comment','No Comment')
                id = x['id']
                #get interface
                interface = x.get('interface','Local')
                int_uuid = self._get_int_uuid(interface,dev_uuid)
                nat_address = None
                nat_inside_id = None
                dns_name = self._get_dns(host,address)
                ip_add = self._write_address(int_uuid,address,comment,status,nat_inside_id,dns_name)
                result = f"name:{address}, {interface},intid:{int_uuid}, comment:{comment}"
                self.log_success(obj=result, message="Added Private IP from NAT")
        for x in all_nats:
            if x.get('action') == 'dst-nat' and x.get('dst-nat') != None:
                address = x.get('dst-address')
                status = status
                comment = x.get('comment','No Comment')
                id = x['id']
                #get interface
                interface = x.get('interface','lo')
                int_uuid = self._get_int_uuid(interface,dev_uuid)
                nat_address = x['to-addresses']
                nat_inside_id = self._get_ip_uuid(nat_address)
                dns_name = self._get_dns(host,address)
                ip_add = self._write_address(int_uuid,address,comment,status,nat_inside_id,dns_name)
                result = f"name:{address}, {interface},intid:{int_uuid}, comment:{comment}"
                self.log_success(obj=result, message="Added Public IP from NAT")


    ## Get IP Addresses ##
    def _get_ipaddrs(self,host):
        api = self._conn_mt(host)
        ips = api.get_resource("/ip/address")
        all_ips = ips.get()
        self.log_success(obj=all_ips, message="Got IP Addresses")
        return all_ips

    def _add_ips(self,host,all_ips,status):
        dev_uuid = self._get_dev_uuid(host)
        try:
            for z in all_ips:
                address = z['address']
                if self._is_private(address) == True:
                    status = Status.objects.get(slug='active')
                    comment = z.get('comment','No Comment')
                    id = z['id']
                    interface = z['interface']
                    nat_address = None
                    int_uuid = self._get_int_uuid(interface,dev_uuid)
                    nat_inside_id = None
                    dns_name = self._get_dns(host,address)
                    ip_add = self._write_address(int_uuid,address,comment,status,nat_inside_id,dns_name)
                    result = f"name:{address}, {interface},intid:{int_uuid}, comment:{comment}"
                    self.log_success(obj=result, message="One of the addresses")
        except:
            raise


    ## Get DNS
    def _get_dns(self,host,address):
        if self._is_private(address) == True:
            api = self._conn_mt(host)
            dns = api.get_resource("/ip/dns/static")
            all_dns = dns.get()
            for x in all_dns:
                if (x['address']==address):
                    local_dns = x['name']
                    self.log_success(obj=local_dns, message="Got Local DNS")
                    return local_dns
                else:
                    return address
        elif self._is_private(address) != True:
            public_dns = socket.getfqdn(address)
            return public_dns
        elif self._is_private(address) == None:
            return "No DNS"


    def _get_dev_uuid(self, switch):
        dev_id	 = Device.objects.get(name=switch)
        dev_uuid =  str(dev_id.id)
        self.log_success(obj=dev_uuid, message="Switch UUID")
        return dev_uuid

    def _get_dev_site(self, switch):
        site_id	 = Device.objects.get(name=switch)
        siteid =  str(site_id.site.id)
        self.log_success(obj=siteid, message="Switch Site ID")
        return siteid

    def _get_int_uuid(self,name, dev_uuid):
        int_id = Interface.objects.filter(name=name, device_id=dev_uuid)
        for res in int_id:
            int_uuid = res.id
            return int_uuid

    def _get_ip_uuid(self,address):
        ip = IPAddress.objects.filter(address=address)
        for x in ip.values():
            ip_uuid = (x['id'])
            return ip_uuid

    def _write_vlan(self,vlan,status,name,siteid):
        try:
            new_vlan = VLAN.objects.update_or_create(
                name=name,
                vid=int(vlan),
                status=status,
                site_id=siteid,
                #group_id=group_id
                    )
            result = new_vlan[0].name
            self.log_success(obj=result, message="New Vlan Added")
            return result
        except:
            #name = self.assignName(vlan,cid)
            self.log_failure(obj=vlan, message="Failed to add Vlan")
            return None

    def _write_int(self,devid,mac,type,name,untagged_vlan_id):
        try:
            new_int = Interface.objects.update_or_create(
                device_id=devid,
                type=type,
                mac_address=str(mac),
                name=name,
                untagged_vlan_id=untagged_vlan_id
            )
            self.log_success(obj=new_int, message="Interface Existed or Created")
            return new_int

        except BaseException as err:
            self.log_failure(message="Failed to add interface")
            raise


    def _write_address(self,int_uuid,address,comment,status,nat_inside_id,dns_name):
        obj_type = ContentType.objects.get(model="interface")
        try:
            new_addr = IPAddress.objects.update_or_create(
                assigned_object_type=obj_type,
                assigned_object_id=int_uuid,
                address=address,
                status=status,
                description=comment,
                #nat_inside = nat_address,
                nat_inside_id=nat_inside_id,
                dns_name=dns_name
                )
            self.log_success(obj=new_addr, message="Address Existed or Created")
            return new_addr
        except BaseException as err:
            self.log_failure(message="Failed to Add Address")
            raise

    def run(self, data, commit):

        switch=(data['device'])
        self.log_success(obj=switch, message="Print Switch")
        fw = switch.last()
        firewall = fw.name

        status = Status.objects.get(slug='active')
        dev_uuid = self._get_dev_uuid(firewall)

        siteid = self._get_dev_site(firewall)


        all_interfaces = self._get_intfs(firewall)
        add_intfs = self._add_intfs(firewall, all_interfaces)
        self.log_success(obj=add_intfs, message="Added Interfaces ")

        all_vlans = self._get_vlans(firewall)
        add_vlans = self._add_vlans(all_vlans,status,siteid,dev_uuid)
        self.log_success(obj=add_vlans, message="Added Vlans ")


        all_ips = self._get_ipaddrs(firewall)
        final_ips = self._add_ips(firewall,all_ips,status)
        self.log_success(obj=final_ips, message="Added IPs ")

        all_nats = self._get_nats(firewall)
        add_nats = self._add_nats(firewall,all_nats,status)
        self.log_success(obj=add_nats, message="Added Internal IP via NAT ")

